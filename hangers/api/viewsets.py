from rest_framework import viewsets

from hangers.api.serializers import HangerSerializer, SensorPointSerializer, CalendarEntrySerializer, \
    TemperatureAtLocationSerializer
from hangers.models import Hanger, SensorPoint, CalendarEntry


class HangerViewSet(viewsets.ModelViewSet):
    queryset = Hanger.objects.all()
    serializer_class = HangerSerializer


class CalendarEntryViewSet(viewsets.ModelViewSet):
    queryset = CalendarEntry.objects.all()
    serializer_class = CalendarEntrySerializer


class SensorPointViewSet(viewsets.ModelViewSet):
    queryset = SensorPoint.objects.all()
    serializer_class = SensorPointSerializer


class TemperatureAtLocation(viewsets.ModelViewSet):
    queryset = SensorPoint.objects.all()
    serializer_class = TemperatureAtLocationSerializer
