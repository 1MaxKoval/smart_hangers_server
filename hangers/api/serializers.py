from rest_framework.serializers import HyperlinkedModelSerializer
from hangers import models


class SensorPointSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = models.SensorPoint
        fields = ['url', 'external_temperature', 'body_temperature', 'latitude', 'longitude', 'bssid']
        extra_kwargs = {
            'url': {'read_only': True},
            'latitude': {'max_digits': 20, 'decimal_places': 15},
            'longitude': {'max_digits': 20, 'decimal_places': 15},
            # TODO: Add a MAC address validator.
            'bssid': {'max_length': 17, 'min_length': 17},
            'external_temperature': {'max_digits': 10, 'decimal_places': 3},
            'body_temperature': {'max_digits': 10, 'decimal_places': 3},
        }


class HangerSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = models.Hanger
        fields = ['url', 'rfid', 'temperature', 'type']
        extra_kwargs = {
            'url': {'read_only': True},
            # TODO: Add a UUID validator.
            'rfid': {'max_length': 36, 'min_length': 36, 'trim_whitespace': True},
            'type': {'max_length': 40, 'min_length': 1},
            'temperature': {'max_digits': 10, 'decimal_places': 3},
        }


class StatusSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = models.Status
        fields = ['url', 'status']


class CalendarEntrySerializer(HyperlinkedModelSerializer):
    class Meta:
        model = models.CalendarEntry
        fields = ['url', 'location_name', 'description', 'date_time', 'latitude', 'longitude']
        extra_kwargs = {
            'url': {'read_only': True},
            'location_name': {'max_length': 100},
            'latitude': {'max_digits': 20, 'decimal_places': 15},
            'longitude': {'max_digits': 20, 'decimal_places': 15},
        }


