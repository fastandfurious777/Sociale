from rest_framework.exceptions import ValidationError, APIException
from django.utils import timezone
from django.db import transaction

from rentals.selectors import rental_get, rental_get_current_by_user
from rentals.models import Rental
from users.selectors import user_get
from bikes.selectors import bike_get
from parkings.selectors import check_parking_location


@transaction.atomic
def rental_start(user_id: int, bike_id: int):
    user = user_get(user_id=user_id)
    bike = bike_get(bike_id=bike_id)

    rental = Rental(
        user=user,
        bike=bike,
        started_at=timezone.now(),
        status=Rental.Status.STARTED
    )

    bike.rent(user)
    bike.full_clean()
    bike.save()

    rental.full_clean()
    rental.save()

    
@transaction.atomic
def rental_finish(user_id: int, lon: float, lat: float):
    rental = rental_get_current_by_user(user_id=user_id)

    rental.status = Rental.Status.FINISHED
    rental.full_clean()
    rental.save()
    if check_parking_location(lon=lon, lat=lat):
        rental.bike.return_bike(lon=lon, lat=lat)
        rental.bike.save()
    else:
        raise APIException(detail={'detail': "You are not in the parking area"}, code=400)



def rental_update(rental_id: int, data):
    rental = rental_get(rental_id=rental_id)
    fields = {'status', 'started_at', 'finished_at'}
    for record in data:
        if record in fields:
            setattr(rental, record, data[record])
        else:
            raise ValidationError(detail={'detail': f"Field '{record}' doesn't exist in 'bike'"})

def rental_delete(rental_id: int):
    rental = rental_get(rental_id=rental_id)
    rental.delete()
