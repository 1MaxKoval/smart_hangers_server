from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from hangers.api.serializers import HangerSerializer, SensorPointSerializer, CalendarEntrySerializer, \
    TemperatureAtLocationSerializer
from hangers.models import Hanger, SensorPoint, CalendarEntry
from datetime import timedelta
from django.utils import timezone


class HangerViewSet(viewsets.ModelViewSet):
    queryset = Hanger.objects.all()
    serializer_class = HangerSerializer

    @action(detail=False, methods=['delete'])
    def delete_all_hangers(self, request):
        Hanger.objects.all().delete()
        return Response({'success': 'deleted all Hanger objects from the database'})


class CalendarEntryViewSet(viewsets.ModelViewSet):
    # Return all entries one hour ahead of UK central time (NL) time.
    queryset = CalendarEntry.objects.filter(date_time__gt=timezone.now() + timedelta(hours=1))
    serializer_class = CalendarEntrySerializer

    @action(detail=False, methods=['delete'])
    def delete_all_events(self, request):
        CalendarEntry.objects.all().delete()
        return Response({'success': 'deleted all events from the calendar'})


class SensorPointViewSet(viewsets.ModelViewSet):
    queryset = SensorPoint.objects.all()
    serializer_class = SensorPointSerializer

    @action(detail=False, methods=['delete'])
    def delete_all_hangers(self, request):
        SensorPoint.objects.all().delete()
        return Response({'success': 'deleted all sensor points'})


class TemperatureAtLocation(viewsets.ModelViewSet):
    queryset = SensorPoint.objects.all()
    serializer_class = TemperatureAtLocationSerializer
