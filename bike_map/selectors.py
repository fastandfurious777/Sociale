from typing import Iterable
from . models import Bike, Parking, Rental
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import get_object_or_404

def bike_list() -> Iterable[Bike]:
    query = Q(is_available=True)
    return Bike.objects.filter(query)

def bike_get(id: int) -> Bike | None:
    return get_object_or_404(Bike, id = id)

#  lll
def parking_list() -> Iterable[Parking]:
    query = Q(is_available=True)
    return Bike.objects.filter(query)

def parking_get(id: int) -> Bike | None:
    return get_object_or_404(Bike, id = id)

def rental_list() -> Iterable[Bike]:
    query = Q(is_available=True)
    return Bike.objects.filter(query)

def rental_get(id: int) -> Bike | None:
    return get_object_or_404(Bike, id = id)