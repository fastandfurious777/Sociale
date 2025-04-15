from django.db.models import QuerySet
from django.http import Http404
from parkings.models import Parking


def parking_list(include_inactive: bool = False) -> QuerySet[Parking]:
    if include_inactive:
        return Parking.objects.all()
    return Parking.objects.filter(is_active=True)


def parking_get(parking_id: int) -> Parking:
    try:
        return Parking.objects.get(id=parking_id)
    except Parking.DoesNotExist:
        raise Http404


def parking_get_by_name(name: str) -> Parking:
    try:
        return Parking.objects.get(name=name)
    except Parking.DoesNotExist:
        raise Http404


def check_parking_location(lon: float, lat: float) -> bool:
    parkings = parking_list()
    for parking in parkings:
        if parking.contains_point(lon=lon, lat=lat):
            return True
    return False
