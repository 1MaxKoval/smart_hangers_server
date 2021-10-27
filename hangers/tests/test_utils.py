from rest_framework.test import APISimpleTestCase, APITestCase
from hangers.models import SensorPoint, CalendarEntry, Hanger, TemperatureAtLocation
from hangers.utils import haversine_formula, find_location, get_soonest_event, recommend_clothing_on_temp, \
    estimate_temperature
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
            'temperature': 15.0,
            'gsr_reading': 100.0,
            'latitude': 52.237979,
            'longitude': 6.840117,
            'mac_address': '3c240a49-a6c2-42d8-b006-9665881e3aaa'
        }
        # Twekkelerveld
        sensor_point2 = {
            'temperature': 20.0,
            'gsr_reading': 100.0,
            'latitude': 52.229335,
            'longitude': 6.857358,
            'mac_address': '3c240a49-a6c2-42d8-b006-9665881e3aaa'
        }
        # SensorPoint with a different mac_address
        sensor_point3 = {
            'temperature': 30.0,
            'gsr_reading': 100.0,
            'latitude': 52.229335,
            'longitude': 6.857358,
            'mac_address': 'C8:1B:E3:07:6F:2E'
        }
        self.sensor_point1 = SensorPoint.objects.create(**sensor_point1)
        self.sensor_point2 = SensorPoint.objects.create(**sensor_point2)
        self.sensor_point3 = SensorPoint.objects.create(**sensor_point3)

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

    def test_recommend_clothing_on_temp(self):
        """
        Asserts the functionality of the recommend_clothing_on_temp function.
        """
        t_shirt = {
            'rfid': '6fcef5f8-db9d-462c-8445-c1784c4b2f3b',
            'lower_bound_temperature': 20.0,
            'upper_bound_temperature': 30.0,
            'type': 't-shirt'
        }
        coat = {
            'rfid': '3c240a49-a6c2-42d8-b006-9665881e3aaa',
            'lower_bound_temperature': -5,
            'upper_bound_temperature': 10,
            'type': 'coat'
        }
        Hanger.objects.create(**t_shirt)
        Hanger.objects.create(**coat)
        stuff = recommend_clothing_on_temp(25)
        self.assertEqual(stuff[0], '6fcef5f8-db9d-462c-8445-c1784c4b2f3b')
        other_stuff = recommend_clothing_on_temp(-3)
        self.assertEqual(other_stuff[0], '3c240a49-a6c2-42d8-b006-9665881e3aaa')

    def test_estimate_temperature(self):
        """
        Asserts the functionality of estimate_temperature function.
        """
        TemperatureAtLocation.objects.create(temperature=30)
        temperature_estimate = estimate_temperature(self.sensor_point1)
        self.assertEqual(temperature_estimate, 26.25)

    def test_estimate_temperature_high_gsr(self):
        """
        Asserts that the estimate_temperature behaves appropriately in the case the GSR is above the threshold value.
        """
        new_sensor_point = {
            'temperature': 15.0,
            'gsr_reading': 150.0,
            'latitude': 52.237979,
            'longitude': 6.840117,
            'mac_address': 'amazing-mac-address'
        }
        new_sensor_point1 = {
            'temperature': 15.0,
            'gsr_reading': 140.0,
            'latitude': 52.237979,
            'longitude': 6.840117,
            'mac_address': 'amazing-mac-address'
        }
        SensorPoint.objects.create(**new_sensor_point1)
        TemperatureAtLocation.objects.create(temperature=30)
        point = SensorPoint.objects.create(**new_sensor_point)
        self.assertEqual(estimate_temperature(point), 30)



