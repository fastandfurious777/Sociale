from . models import Bike, Rental, Parking
from django.contrib.auth.models import User
from typing import  Any, Dict, Iterable
from rest_framework.exceptions import ValidationError, APIException # type: ignore
from django.shortcuts import get_object_or_404
from django.utils import timezone
from . selectors import user_get, bike_get, rental_get, rental_get_current
from cryptography import fernet
from Sociale.settings import CIPHER_KEY
from datetime import datetime
from utils import date_validate, parking_location_validate

def bike_create(*,name: str, lon: float, lat: float, code: str, is_available: bool) -> Bike:
    if isinstance(CIPHER_KEY, str):
        key = CIPHER_KEY.encode()
    else:
        raise APIException("CIPHER_KEY must be a string")
    
    cipher = fernet.Fernet(key)
    enrypted_code = cipher.encrypt(code.encode())

    # Encrypted code will be store as string as 'code' is a TextField
    enrypted_code = enrypted_code.decode()

    bike = Bike(name=name,lon=lon,lat=lat,code=enrypted_code, is_available=is_available)

    # 'Full clean' method calls 'clean' along with other validation methods
    bike.full_clean()
    bike.save()
    return bike

def bike_update(id: int, data: Dict[str, Any]) -> Bike:
    bike = bike_get(id=id)
    fields: list[str] = ['name', 'lon', 'lat', 'is_available', 'last_taken_by'] 
    for record in data:
        if record in fields:
            if record == 'last_taken_by':
                user = user_get(id=data[record])
                setattr(bike, 'last_taken_by', user)
            else:
                setattr(bike, record, data[record])   
        else:
            raise ValidationError({'detail':f"Field '{record}' doesnt exist in 'bike' "})
    bike.full_clean()
    bike.save()
    return bike

def bike_delete(id: int) -> None:
    bike = get_object_or_404(Bike, id = id)
    bike.delete()

def rental_create(user_id: int, bike_id: int) -> None:
        start_time: datetime = timezone.now()
        bike: Bike = bike_get(id=bike_id)
        user: User = user_get(id=user_id)

        rental = Rental(user=user, bike=bike, started_at=start_time)
        rental.full_clean()

        bike_update(id=bike_id, data={'is_available':False, 'user':user_id})
        
        rental.save()

def rental_update(id: int, data: Dict[str, Any]) -> None:
    rental = rental_get(id=id)

    if data['user_id'] is not None:
        user = user_get(id=data['user'])
        rental.user = user
    if data['bike_id'] is not None:
        bike = bike_get(id=data['bike'])
        rental.bike = bike
    if data['started_at'] is not None:
        started_at: datetime = date_validate(data['started_at'])
        rental.started_at = started_at
    if data['finished_at'] is not None:
        finished_at: datetime = date_validate(data['finished_at'])
        rental.started_at = finished_at

    rental.full_clean()

    rental.save()


def rental_start(user_id: int, bike_id: int) -> None:
        rental_create(user_id=user_id, bike_id=bike_id)

        bike_update(id=bike_id, data={'is_available':False, 'user':user_id})
         
def rental_finish(user_id: int, bike_id: int, lon: float, lat: float) -> None:
        parkings: Iterable[Parking] = Parking.objects.all()
        if not parking_location_validate(lon, lat, parkings):
            raise APIException("Invalid parking location",403)
             
        rental: Rental = rental_get_current(started_by=user_id)

        rental_data: dict[str, int | datetime]={
        'user_id':user_id,
        'bike_id':bike_id, 
        'finished_at': timezone.now()
        }
        rental_update(id=rental.id, data=rental_data) # type: ignore
        
        bike_data: dict[ str, float | bool] = {
        'lon':lon, 'lat':lat,
        'is_available':True, 
        'user':user_id
        }
        bike_update(id=bike_id, data=bike_data)
         


      