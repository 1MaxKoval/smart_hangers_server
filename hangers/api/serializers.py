from rest_framework.serializers import HyperlinkedModelSerializer, ModelSerializer
from hangers import models


class SensorPointSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = models.SensorPoint
        fields = ['url', 'temperature', 'gsr_reading', 'latitude', 'longitude', 'bssid']
        extra_kwargs = {
            'url': {'read_only': True},
            'bssid': {'max_length': 17, 'min_length': 17},
        }


class HangerSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = models.Hanger
        fields = ['url', 'rfid', 'lower_bound_temperature', 'upper_bound_temperature', 'type']
        extra_kwargs = {
            'url': {'read_only': True},
            # TODO: Add a UUID validator.
            'rfid': {'max_length': 36, 'min_length': 36, 'trim_whitespace': True},
            'type': {'max_length': 40, 'min_length': 1},
        }


class StatusSerializer(ModelSerializer):
    class Meta:
        model = models.Status
        fields = ['status']


class CalendarEntrySerializer(HyperlinkedModelSerializer):
    class Meta:
        model = models.CalendarEntry
        fields = ['url', 'location_name', 'description', 'date_time', 'latitude', 'longitude']
        extra_kwargs = {
            'url': {'read_only': True},
            'location_name': {'max_length': 100},
        }


class TemperatureAtLocationSerializer(ModelSerializer):
    class Meta:
        model = models.TemperatureAtLocation
        fields = ['temperature']
