from rest_framework.exceptions import APIException
from django.db.models import Q
from django.http import Http404

from rentals.models import Rental
from users.selectors import user_get

def rental_list(user_id: int , status: str):
    query = Q()
    if user_id is not None:
        user = user_get(user_id=user_id)
        query &= Q(user=user)

    if status is not None:
        query &= Q(status=Rental.Status[status])

    return Rental.objects.filter(query)

def rental_get(rental_id: int):
    try:
        return Rental.objects.get(id=rental_id)
    except Rental.DoesNotExist:
        raise Http404("Rental not found")

def rental_get_current_by_user(user_id: int) -> Rental | None:
    user = user_get(user_id=user_id)
    query = Q(user=user, status=Rental.Status.STARTED)
    try:
        return Rental.objects.get(query)
    except Rental.DoesNotExist:
        return None
    except Rental.MultipleObjectsReturned:
        raise APIException(f"User has multiple rentals active")