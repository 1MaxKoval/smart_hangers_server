from django.urls import path, include
from rest_framework import routers
from hangers import views
from hangers.api import viewsets

urlpatterns = [
    path('temperature', views.TemperatureAtLocationView.as_view()),
    path('status', views.StatusView.as_view()),
    path('recommendations', views.recommendations),
    path('temperature_estimate', views.temperature_estimate),
]

# Registering the ViewSets
router = routers.SimpleRouter(trailing_slash=False)
router.register(r'hangers', viewsets.HangerViewSet)
router.register(r'sensor_data', viewsets.SensorPointViewSet)
router.register(r'calendar', viewsets.CalendarEntryViewSet)
# Add it to existing urls
urlpatterns += router.urls


