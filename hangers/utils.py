from hangers.models import CalendarEntry
from decimal import Decimal
from typing import List, Tuple
import math

# Radius of the Earth
R = 6381e3


def recommend_clothing() -> List[str]:
    """
    Returns a list of clothing RFIDs depending on the upcoming event set in the Calendar.
    """
    # TODO: Get a CalendarEvent and read its location.
    pass


def calculate_difference(location_a: Tuple[float, float], location_b: Tuple[float, float]) -> float:
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


def haversine_formula():
    pass
