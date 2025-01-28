from . models import User
from . selectors import user_get
from django.db import transaction
from rest_framework.exceptions import ValidationError


def user_create(*, email: str, password: str, first_name: str, last_name) -> User:

    user: User = User.objects.create_user(email=email, password=password, first_name=first_name, last_name=last_name)

    return user


def user_update(user_id: int, data: dict[str, str | bool]) -> User | None:
    user = user_get(user_id=user_id)
    if user is None:
        return None
    
    fields: list[str] = ['email', 'first_name', 'last_name', 'is_active', 'is_verified'] 
    for record in data:
        if record in fields:
            setattr(user, record, data[record])
        else:
            # TODO add logger , validation error shouldn't give to much info in production 
            # raise ValidationError({'detail': f"Field '{record}' is not meant to be updated"})
            return None

    user.full_clean()
    user.save()
    return user
        
def user_delete(user_id: int) -> dict[int | str] | None:
    user = user_get(user_id=user_id)
    if user is None:
        return None
    
    user_data = {
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
    }

    user.delete()
    return user_data