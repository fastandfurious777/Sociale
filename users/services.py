from rest_framework.exceptions import ValidationError
from users.models import User
from users.selectors import user_get


def user_create(*, email: str, password: str, first_name: str, last_name) -> User:

    user = User.objects.create_user(
        email=email, password=password, first_name=first_name, last_name=last_name
    )

    return user


def user_update(user_id: int, data: dict[str, str | bool]) -> None:
    user = user_get(user_id=user_id)

    fields: set[str] = {"email", "first_name", "last_name", "is_active", "is_verified"}
    for record in data:
        if record in fields:
            setattr(user, record, data[record])
        else:
            raise ValidationError(
                {"detail": f"Field '{record}' is not meant to be updated"}
            )

    user.full_clean()
    user.save()


def user_delete(user_id: int) -> None:
    user = user_get(user_id=user_id)
    user.delete()
