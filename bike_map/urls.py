from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="map-home"),
     path('bike-positions/', views.bike_positions, name="bike-positions"),

]