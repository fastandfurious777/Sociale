from django.db.models import QuerySet
from users.models import User
from django.http import Http404


def user_list() -> QuerySet[User]:
    return User.objects.all()


def user_get(user_id: int) -> User:
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise Http404


def user_get_by_email(email: int) -> User:
    try:
        return User.objects.get(email=email)
    except User.DoesNotExist:
        raise Http404
