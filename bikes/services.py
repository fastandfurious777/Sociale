from bikes.selectors import bike_get
from users.selectors import user_get
from rest_framework.exceptions import ValidationError
from bikes.models import Bike
from typing import Any

def bike_create(
    *,
    name: str,
    lon: float,
    lat: float,
    code: str,
    is_available: bool,
    last_taken_by: int = None
) -> None:
    
    bike = Bike(
        name=name,
        lon=lon,
        lat=lat,
        code=code,
        is_available=is_available,
        last_taken_by=last_taken_by
    )
    bike.full_clean()
    bike.save()


def bike_update(bike_id: int, data: dict[str, Any]) -> None:
    bike: Bike = bike_get(bike_id=bike_id)
    fields: list[str] = ['name', 'lon', 'lat', 'code', 'is_available', 'last_taken_by']
    
    for record in data:
        if record in fields:
            if record == 'last_taken_by':
                user = user_get(user_id=data[record])
                print(user)
                setattr(bike, 'last_taken_by', user)
            else:
                setattr(bike, record, data[record])
        else:
            raise ValidationError(detail={'detail': f"Field '{record}' doesn't exist in 'bike'"})
    
    bike.full_clean()
    bike.save()


def bike_delete(bike_id: int) -> None:
    bike = bike_get(bike_id=bike_id)
    bike.delete()