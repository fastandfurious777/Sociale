from . models import User
from . selectors import user_get
from django.db import transaction
from rest_framework.exceptions import ValidationError

@transaction.atomic
def user_create(*, email: str, password: str) -> User:

    user: User = User.objects.create_user(email=email, password=password)

    return user

@transaction.atomic
def user_update(id: int, data: dict[str, str | bool]) -> User:
    user = user_get(id=id)
    fields: list[str] = ['email', 'first_name', 'last_name', 'is_active', 'is_verified'] 

    for record in data:
        if record in fields:
            setattr(user, record, data[record])
        else:
            # TODO add logger , validation error shouldn't give to much info in production 
            raise ValidationError({'detail':f"Field '{record}' is not meant to be updated"})
        
    user.full_clean()
    user.save()
    return user
        

def user_delete(id: int):
    user = user_get(id=id)

    user.delete()