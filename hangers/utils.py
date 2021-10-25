from hangers.models import CalendarEntry, SensorPoint
from decimal import Decimal
from typing import List, Tuple, Optional
import math

# Radius of the Earth
R = 6381e3


def recommend_clothing() -> List[str]:
    """
    Returns a list of clothing RFIDs depending on the upcoming event set in the Calendar.
    """
    # TODO: Get a CalendarEvent and read its location.
    pass


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
            if smallest_distance is None:
                smallest_distance = d_distance
                closest_point = rows[i]
            elif d_distance < smallest_distance:
                smallest_distance = d_distance
                closest_point = rows[i]
    return closest_point






def recommend_clothing_on_temp(temperature: float = None) -> List[str]:
    """
    Get clothing from the database based on the temperature the user recorded previously.

    """


def haversine_formula(location_a: Tuple[float, float], location_b: Tuple[float, float]) -> float:
    """
    Given 2 coordinates (latitude, longitude) calculates the shortest distance between them.
    """

    # Reading latitude and longitude
    phi_1, lambda_1 = location_a[0] * math.pi / 180, location_a[1] * math.pi / 180
    phi_2, lambda_2 = location_b[0] * math.pi / 180, location_b[1] * math.pi / 180

    # Calculate difference
    d_phi = phi_2 - phi_1
    d_lambda = lambda_2 - lambda_1
    # Apply haversine http://www.movable-type.co.uk/scripts/latlong.html
    a = math.sin(d_phi / 2) * math.sin(d_phi / 2) + math.cos(phi_1) * math.cos(phi_2) * math.sin(
        d_lambda / 2) * math.sin(d_lambda / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    # Distance in meters
    d = R * c
    return d
