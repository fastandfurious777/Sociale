from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="map-home"),
    path('scanner/', views.scanner, name="scanner"),
    path('bikes/', views.bike_list, name='bike-list'),
    path('bikes/<int:id>', views.bike_management, name="bike-management"),
    path('polygons/', views.polygon_list, name="polygon-list"),
    path('polygons/<int:id>', views.polygon_management, name="polygon-management"),
    path('get-user-status/', views.get_user_status, name="get-user-status"),
    path('get-bike-code/', views.get_bike_code, name='get-bike-code'),
    path('start-rental/', views.start_rental, name='start-rental'),
    path('end-rental/', views.end_rental, name='end-rental'),

]