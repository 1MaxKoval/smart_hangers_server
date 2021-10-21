from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from hangers.models import Hanger, SensorPoint, Status, CalendarEntry
from hangers.api.serializers import HangerSerializer, SensorPointSerializer, CalendarEntrySerializer, StatusSerializer


class HangerViewSet(viewsets.ModelViewSet):
    queryset = Hanger.objects.all()
    serializer_class = HangerSerializer


class CalendarEntryViewSet(viewsets.ModelViewSet):
    queryset = CalendarEntry.objects.all()
    serializer_class = CalendarEntrySerializer


class SensorPointViewSet(viewsets.ModelViewSet):
    queryset = SensorPoint.objects.all()
    serializer_class = SensorPointSerializer



