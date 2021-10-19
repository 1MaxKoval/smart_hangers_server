from django.urls import path, include
from hangers import views

urlpatterns = [
    path('hello_world', views.hello_view),
]
