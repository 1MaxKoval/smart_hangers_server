from django.db import models


class SensorPoint(models.Model):
    external_temperature = models.DecimalField(max_digits=10, decimal_places=3)
    body_temperature = models.DecimalField(max_digits=10, decimal_places=3)
    latitude = models.DecimalField(max_digits=20, decimal_places=15)
    longitude = models.DecimalField(max_digits=20, decimal_places=15)
    bssid = models.CharField(max_length=17)


class Hanger(models.Model):
    rfid = models.CharField(max_length=36)
    temperature = models.DecimalField(max_digits=10, decimal_places=3)
    type = models.CharField(max_length=40)


class Status(models.Model):
    status = models.BooleanField()


class CalendarEntry(models.Model):
    class Meta:
        ordering = ['date_time']
    location_name = models.CharField(max_length=100)
    description = models.TextField()
    date_time = models.DateTimeField()
    latitude = models.DecimalField(max_digits=20, decimal_places=15)
    longitude = models.DecimalField(max_digits=20, decimal_places=15)

