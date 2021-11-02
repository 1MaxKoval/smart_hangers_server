from rest_framework import viewsets

from hangers.api.serializers import HangerSerializer, SensorPointSerializer, CalendarEntrySerializer, \
    TemperatureAtLocationSerializer
from hangers.models import Hanger, SensorPoint, CalendarEntry
from datetime import timedelta
from django.utils import timezone


class HangerViewSet(viewsets.ModelViewSet):
    queryset = Hanger.objects.all()
    serializer_class = HangerSerializer


class CalendarEntryViewSet(viewsets.ModelViewSet):
    # Return all entries one hour ahead of UK central time (NL) time.
    queryset = CalendarEntry.objects.filter(date_time__gt=timezone.now()+timedelta(hours=1))
    serializer_class = CalendarEntrySerializer


class SensorPointViewSet(viewsets.ModelViewSet):
    queryset = SensorPoint.objects.all()
    serializer_class = SensorPointSerializer


class TemperatureAtLocation(viewsets.ModelViewSet):
    queryset = SensorPoint.objects.all()
    serializer_class = TemperatureAtLocationSerializer
