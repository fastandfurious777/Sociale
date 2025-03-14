from bikes.models import Bike
from django.db.models import QuerySet
from django.http import Http404
from rest_framework.exceptions import APIException

def bike_list(include_unavailable=False) -> QuerySet[Bike]:
    if include_unavailable:
        return Bike.objects.all()
    else:
        return Bike.objects.filter(is_available=True)

def bike_get(bike_id: int) -> Bike:
    try:
        return Bike.objects.get(id=bike_id)
    except Bike.DoesNotExist:
        raise Http404("Bike not found")
    
def bike_get_by_qrcode(qr_code) -> Bike:
    try:
        return Bike.objects.get(qr_code=qr_code)
    except Bike.DoesNotExist:
        raise Http404("Bike not found")
    except Bike.MultipleObjectsReturned:
        # TODO add logger with critical error

        # APIException is by default handled as SERVER_ERROR with status code 500
        raise APIException
    