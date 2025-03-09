from bikes.models import Bike
from django.db.models import QuerySet
from django.http import Http404

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