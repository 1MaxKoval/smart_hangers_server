from rest_framework.test import APISimpleTestCase, APITestCase
from hangers.models import SensorPoint, CalendarEntry
from hangers.utils import haversine_formula, find_location, get_soonest_event
from datetime import timedelta
from django.utils import timezone
import unittest


# SF : 37.760154, -122.450575
# NY : 40.712498, -74.006886
# Distance: 4132km

# Twente Field: 52.241476, 6.849384
# Kennis Park:  52.237973, 6.840168

class TestCalculations(APISimpleTestCase):

    def setUp(self):
        pass

    def test_calculate_difference_big(self):
        z = haversine_formula((37.760154, -122.450575), (40.712498, -74.006886))

    def test_calculate_difference_smol(self):
        z = haversine_formula((52.241476, 6.849384), (52.237973, 6.840168))


class TestRecommendations(APITestCase):

    def setUp(self):
        # Kennis Park
        sensor_point1 = {
            'temperature': 25.0,
            'gsr_reading': 36.0,
            'latitude': 52.237979,
            'longitude': 6.840117
        }
        # Twekkelerveld
        sensor_point2 = {
            'temperature': 25.0,
            'gsr_reading': 36.0,
            'latitude': 52.229335,
            'longitude': 6.857358
        }
        SensorPoint.objects.create(**sensor_point1)
        SensorPoint.objects.create(**sensor_point2)

    def test_find_location_no_close_point(self):
        # Road leading from Spiegel to Ravelijn.
        location = (52.238866, 6.852006)
        related_location = find_location(location)
        self.assertEqual(None, related_location)

    def test_find_location_closest_point(self):
        """
        Assert that find_location function output the closest SensorData in the case multiple points are located within
        the 500m range of the specified location.
        """
        location = (52.237788, 6.840311)
        closest_to_location = {
            'temperature': 25.0,
            'gsr_reading': 36.0,
            'latitude': 52.237768,
            'longitude': 6.840477
        }
        SensorPoint.objects.create(**closest_to_location)
        related_location = find_location(location)
        self.assertEqual(float(related_location.latitude), 52.237768)
        self.assertEqual(float(related_location.longitude), 6.840477)

    def test_get_soonest_event(self):
        """
        Asserts that get_soonest_event retrieves the soonest event from the database relative to the current time.
        """
        now = timezone.now()
        datetime1 = now + timedelta(hours=2)
        datetime2 = now + timedelta(hours=3)
        datetime3 = now - timedelta(hours=2)
        entry1 = {
            'location_name': 'soonest_event',
            'description': 'some_description',
            'date_time': datetime1,
            'latitude': 2.334,
            'longitude': 3.23122
        }
        entry2 = {
            'location_name': 'some_name',
            'description': 'some_description',
            'date_time': datetime2,
            'latitude': 2.334,
            'longitude': 3.23122
        }
        entry3 = {
            'location_name': 'some_name',
            'description': 'some_description',
            'date_time': datetime3,
            'latitude': 2.334,
            'longitude': 3.23122
        }
        CalendarEntry.objects.create(**entry1)
        CalendarEntry.objects.create(**entry2)
        CalendarEntry.objects.create(**entry3)
        event = get_soonest_event()
        self.assertEquals(event.date_time, datetime1)