from rest_framework.serializers import HyperlinkedModelSerializer, ModelSerializer
from hangers import models


class SensorPointSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = models.SensorPoint
        fields = ['url', 'temperature', 'gsr_reading', 'latitude', 'longitude', 'mac_address']
        extra_kwargs = {
            'url': {'read_only': True},
        }


class HangerSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = models.Hanger
        fields = ['url', 'rfid', 'lower_bound_temperature', 'upper_bound_temperature', 'type']
        extra_kwargs = {
            'url': {'read_only': True},
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
        }


class TemperatureAtLocationSerializer(ModelSerializer):
    class Meta:
        model = models.TemperatureAtLocation
        fields = ['temperature']
