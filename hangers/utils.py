from rest_framework import status
from hangers.models import CalendarEntry, SensorPoint, TemperatureAtLocation, Hanger
from hangers.api.exceptions import HangerAppError
from typing import List, Tuple, Optional
from django.utils import timezone
import math

# Radius of the Earth
R = 6381e3


def recommend_clothing() -> List[str]:
    """
    Returns a list of clothing RFIDs depending on the upcoming event set in the Calendar.

    Raises
    ------
    HangerAppError
        See the other functions in this file

    """
    event = get_soonest_event()
    closest_sensor_point = find_location((event.latitude, event.longitude))
    if closest_sensor_point is None:
        return list()
    else:
        clothing = recommend_clothing_on_temp(estimate_temperature(closest_sensor_point))
        return clothing


def recommend_clothing_on_temp(temperature: float = None) -> List[str]:
    """
    Get clothing from the database based on the temperature the user recorded previously.

    Filters through the clothing in the database by seeing if the given temperature value falls within the temperature
    range of those clothes.

    Returns
    -------
    List[str]
        A list of UIDs of clothes

    """
    first_filter = Hanger.objects.filter(lower_bound_temperature__lte=temperature)
    appropriate_clothing = first_filter.filter(upper_bound_temperature__gte=temperature)
    return [piece_of_clothing.rfid for piece_of_clothing in appropriate_clothing]


def get_environment_temperature(location: Tuple[float, float]) -> float:
    """
    Retrieves the temperature of the environment at a given location.

    Raises
    ------
    HangerAppError
        Thrown in the case the server is not able to fetch the temperature of the environment.
    """
    environment_temperatures = TemperatureAtLocation.objects.all()
    if len(environment_temperatures) != 0:
        location_temp_obj = environment_temperatures[0]
    else:
        raise HangerAppError(detail={'error': 'Unable to fetch environment temperature'},
                             code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return location_temp_obj.temperature


def estimate_temperature(point: SensorPoint) -> float:
    """
    Estimates the temperature that the clothing should be suitable for.
    """
    environment_temperature = get_environment_temperature((point.latitude, point.longitude))
    objects_with_the_same_bssid = SensorPoint.objects.filter(mac_address__icontains=point.mac_address)
    total_temperature = 0
    total_gsr = 0
    for sensor_point in objects_with_the_same_bssid:
        total_temperature += sensor_point.temperature
        total_gsr += sensor_point.gsr_reading
    avg_temp = total_temperature / len(objects_with_the_same_bssid)
    avg_gsr = total_gsr / len(objects_with_the_same_bssid)
    # Get the outside temperature from the 'API'
    if avg_gsr >= 130:
        temperature_estimate = environment_temperature + 10
    else:
        temperature_estimate = (environment_temperature * 0.7) + (avg_temp * 0.3)
    # Returns the weighted average of both values
    return temperature_estimate


def find_location(location: Tuple[float, float]) -> Optional[SensorPoint]:
    """
    Perform a linear search on the SensorPoint table and find the SensorPoint instance closest to the provided location.

    The algorithm ignores the points that are more than 500m away from the location. In case no SensorPoint is within
    the 500m radius of the location returns None.

    Returns
    -------
    None
        Case no point within 500m radius.
    SensorPoint
        A 'row' in the SensorPoint table.
    """

    # Get all rows
    rows = SensorPoint.objects.all()
    # Case the database is empty
    if len(rows) == 0:
        return None
    smallest_distance = None
    closest_point = None
    for i in range(0, len(rows)):
        d_distance = haversine_formula(location, (float(rows[i].latitude), float(rows[i].longitude)))
        if d_distance < 500.0:
            if smallest_distance is None or d_distance < smallest_distance:
                smallest_distance = d_distance
                closest_point = rows[i]
    return closest_point


def haversine_formula(location_a: Tuple[float, float], location_b: Tuple[float, float]) -> float:
    """
    Given 2 coordinates (latitude, longitude) calculates the shortest distance between them.

    Haversine formula
    """

    # Reading latitude and longitude
    phi_1, lambda_1 = location_a[0] * math.pi / 180, location_a[1] * math.pi / 180
    phi_2, lambda_2 = location_b[0] * math.pi / 180, location_b[1] * math.pi / 180

    # Calculate difference
    d_phi = phi_2 - phi_1
    d_lambda = lambda_2 - lambda_1
    # Apply haversine
    a = math.sin(d_phi / 2) * math.sin(d_phi / 2) + math.cos(phi_1) * math.cos(phi_2) * math.sin(
        d_lambda / 2) * math.sin(d_lambda / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    # Distance in meters
    d = R * c
    return d


def get_soonest_event() -> CalendarEntry:
    """
    Retrieves the soonest event from the database.

    Returns
    -------
    None
        Case there are no upcoming events
    CalendarEntry
        Entry of the soonest upcoming event

    Raises
    ------
    HangerAppError
        Raised in the case there are no CalendarEvents in the database
    """
    entries = CalendarEntry.objects.filter(date_time__gt=timezone.now())
    if len(entries) == 0:
        raise HangerAppError(detail={'error': 'There are no upcoming events in the calendar!'},
                             code=status.HTTP_404_NOT_FOUND)
    else:
        # Since CalendarEntry is sorted by the meta option on the model
        return entries[0]
