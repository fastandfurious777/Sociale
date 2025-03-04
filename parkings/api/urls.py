from django.urls import path

from . views import (
    ParkingListApi,
    ParkingDetailApi,
    ParkingCreateApi,
    ParkingUpdateApi,
    ParkingDeleteApi
)

app_name = 'parkings'

urlpatterns = [ 
    path('', ParkingListApi.as_view(), name='list'),
    path('create/', ParkingCreateApi.as_view(), name='create'),
    path('<int:parking_id>/', ParkingDetailApi.as_view(), name='detail'),
    path('<int:parking_id>/update/', ParkingUpdateApi.as_view(), name='update'),
    path('<int:parking_id>/delete/', ParkingDeleteApi.as_view(), name='delete'),
]