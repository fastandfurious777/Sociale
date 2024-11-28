from django.urls import path, include
from . apis.bikes import (
    BikeListApi,
    BikeDetailApi,
    BikeCreateApi,
    BikeUpdateApi,
    BikeDeleteApi
)
from . apis.parkings import (
    ParkingListApi,
    ParkingDetailApi,
    ParkingCreateApi,
    ParkingUpdateApi,
    ParkingDeleteApi
)
from . apis.rentals import (
    RentalListApi,
    RentalDetailApi,
    RentalCreateApi,
    RentalUpdateApi,
    RentalDeleteApi
)

urlpatterns = [ 
    path('',  BikeListApi.as_view()),
    path('<int:bike_id>/', BikeDetailApi.as_view())
]

bike_patterns = [ 
    path('', BikeListApi.as_view(), name='list'),
    path('<int:bike_id>/', BikeDetailApi.as_view(), name='detail'),
    path('create/', BikeCreateApi.as_view(), name='create'),
    path('<int:bike_id>/update/', BikeUpdateApi.as_view(), name='update'),
    path('<int:bike_id>/delete/',BikeDeleteApi.as_view(),name='delete')
]

rental_patterns = [ 
    path('', RentalListApi.as_view(), name='list'),
    path('<int:rental_id>/', RentalDetailApi.as_view(), name='detail'),
    path('create/', RentalCreateApi.as_view(), name='create'),
    path('<int:rental_id>/update/', RentalUpdateApi.as_view(), name='update'),
    path('<int:rental_id>/delete/',RentalDeleteApi.as_view(),name='delete')
]

parking_patterns = [ 
    path('', ParkingListApi.as_view(), name='list'),
    path('<int:parking_id>/', ParkingDetailApi.as_view(), name='detail'),
    path('create/', ParkingCreateApi.as_view(), name='create'),
    path('<int:parking_id>/update/', ParkingUpdateApi.as_view(), name='update'),
    path('<int:parking_id>/delete/',ParkingDeleteApi.as_view(),name='delete')
]

urlpatterns = [
    path('bikes/', include((bike_patterns, 'bikes'))),
    path('parkings/', include((parking_patterns, 'parkings'))),
    path('rentals/', include((rental_patterns, 'rentals'))),
]