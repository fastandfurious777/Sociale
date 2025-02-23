from . models import Parking
from django.db.models import QuerySet
from django.http import Http404

def parking_list() -> QuerySet[Parking]:
    return Parking.objects.all()

def parking_list_active() -> QuerySet[Parking]:
    return Parking.objects.filter(is_active=True)

def parking_get(parking_id: int) -> Parking | None:
    try:
        return Parking.objects.get(id=parking_id)
    except Parking.DoesNotExist:
        raise Http404()

def check_parking_location(lon: float, lat: float) -> bool:
    parkings = parking_list_active()

    for parking in parkings:
        if parking.contains_point(lon=lon, lat=lat):
            return True
    return False



