from . models import Bike
from typing import  Any, Dict
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
def bike_create(*,name: str, lon: float, lat: float, is_available: bool) -> Bike:
    bike = Bike(name=name,lon=lon,lat=lat,is_available=is_available)
    # 'Full clean' method calls 'clean' along with other validation methods
    bike.full_clean()
    bike.save()
    return bike

def bike_update(*, id: int, data: Dict[str, Any]) -> Bike:
    bike = get_object_or_404(Bike, id = id)
    fields: list[str] = ['name', 'lon', 'lat', 'is_available', 'user'] 
    for record in data:
        if record in fields:
            setattr(bike, record, data[record])
        else:
            pass
            # raise ?
    bike.full_clean()
    bike.save()
    return bike

def bike_delete(id: int) -> None:
    bike = get_object_or_404(Bike, id = id)
    print(bike)
    bike.delete()