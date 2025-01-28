from django.db.models import Q, QuerySet
from . models import User

def user_list() -> QuerySet[User]:
    return User.objects.all()

def user_get(user_id: int) -> User | None:
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None
    
def user_get_by_email(email: int) -> User | None:
    try:
        return User.objects.get(email=email)
    except User.DoesNotExist:
        return None