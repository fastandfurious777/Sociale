from typing import Iterable
from . models import Bike, Parking, Rental
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.exceptions import APIException
from django.http import Http404

def user_list() -> Iterable[User]:
    return User.objects.all()

def user_get(id: int) -> User:
    return get_object_or_404(User,id=id)

def bike_list() -> Iterable[Bike]:
    query: Q = Q(is_available=True)
    return Bike.objects.filter(query)

def bike_get(id: int) -> Bike:
    return get_object_or_404(Bike, id = id)

def parking_list() -> Iterable[Parking]:
    return Parking.objects.all()

def parking_get(id: int) -> Parking:
    return get_object_or_404(Parking, id = id)

def rental_list() -> Iterable[Rental]:
    return Rental.objects.all()

def rental_get(id: int) -> Rental:
    return get_object_or_404(Rental, id = id)

def rental_get_current(started_by: int) -> Rental:
    """Gets active rental for a client"""
    user: User = user_get(id=started_by)
    query: Q = Q(finished_at=None,user=user)

    try:
        rental: Rental = Rental.objects.get(query)
    except Rental.DoesNotExist:
        raise Http404
    except Rental.MultipleObjectsReturned:
        raise APIException({"detail": "User has more than one rentals active"})
    
    return rental