from django.db import models


class SensorPoint(models.Model):
    temperature = models.FloatField()
    gsr_reading = models.FloatField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    bssid = models.CharField(max_length=17)


class Hanger(models.Model):
    rfid = models.CharField(max_length=36)
    lower_bound_temperature = models.FloatField()
    upper_bound_temperature = models.FloatField()
    type = models.CharField(max_length=40)


class Status(models.Model):
    status = models.BooleanField()


class CalendarEntry(models.Model):
    class Meta:
        ordering = ['date_time']
    location_name = models.CharField(max_length=100)
    description = models.TextField()
    date_time = models.DateTimeField()
    latitude = models.FloatField()
    longitude = models.FloatField()


class TemperatureAtLocation(models.Model):
    temperature = models.FloatField()

