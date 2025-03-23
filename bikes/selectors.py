from django.db.models import QuerySet
from django.http import Http404
from bikes.models import Bike


def bike_list(include_unavailable: bool = False) -> QuerySet[Bike]:
    if include_unavailable:
        return Bike.objects.all()
    return Bike.objects.filter(is_available=True)


def bike_get(bike_id: int) -> Bike:
    try:
        return Bike.objects.get(id=bike_id)
    except Bike.DoesNotExist:
        raise Http404


def bike_get_by_qrcode(qr_code: str) -> Bike:
    try:
        return Bike.objects.get(qr_code=qr_code)
    except Bike.DoesNotExist:
        raise Http404
