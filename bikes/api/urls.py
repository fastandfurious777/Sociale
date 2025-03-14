from django.urls import path
from .views import (
    BikeListAPI,
    BikeDetailAPI,
    BikeCreateAPI,
    BikeUpdateAPI,
    BikeDeleteAPI
)

app_name = 'bikes'

urlpatterns = [ 
    path('', BikeListAPI.as_view(), name='list'),
    path('create/', BikeCreateAPI.as_view(), name='create'),
    path('<int:bike_id>/', BikeDetailAPI.as_view(), name='detail'),
    path('<int:bike_id>/update/', BikeUpdateAPI.as_view(), name='update'),
    path('<int:bike_id>/delete/', BikeDeleteAPI.as_view(), name='delete'),
]