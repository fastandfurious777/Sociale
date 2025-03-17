from django.urls import path

from rentals.api.views import (
    RentalListAPI,
    RentalDetailAPI,
    RentalStartAPI,
    RentalFinishAPI,
    RentalUpdateAPI,
    RentalDeleteAPI
)

app_name = 'rentals'

urlpatterns = [ 
    path('', RentalListAPI.as_view(), name='list'),
    path('start/', RentalStartAPI.as_view(), name='start'),
    path('finish/', RentalFinishAPI.as_view(), name='finish'),
    path('<int:rental_id>/', RentalDetailAPI.as_view(), name='detail'),
    path('<int:rental_id>/update/', RentalUpdateAPI.as_view(), name='update'),
    path('<int:rental_id>/delete/', RentalDeleteAPI.as_view(), name='delete'),
]