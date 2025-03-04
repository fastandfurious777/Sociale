from . selectors import parking_get
from . models import Parking
from rest_framework.exceptions import ValidationError

def parking_create(*, name: str, area: dict[str], capacity: int = 10, is_active: bool = True) -> None:
    parking = Parking(
        name=name,
        area=area,
        capacity=capacity,
        is_active=is_active
    )
    
    parking.full_clean()
    parking.save()

def parking_update(parking_id: int, data: dict[str]) -> None:
    parking = parking_get(parking_id=parking_id)

    fields: list[str] = ['name', 'area', 'capacity', 'is_active'] 
    for record in data:
        if record in fields:
            setattr(parking, record, data[record])
        else:
            raise ValidationError({'detail': f"Field '{record}' is not meant to be updated"})

    parking.full_clean()

    parking.save()

def parking_delete(parking_id: int) -> None:
    parking = parking_get(parking_id=parking_id)
    parking.delete()