from rest_framework.response import Response # type: ignore
from rest_framework.request import Request # type: ignore
from rest_framework import serializers, status # type: ignore
from rest_framework.views import APIView # type: ignore
from base.selectors import user_list, user_get
from base.services import user_create, user_update, user_delete
from typing import Iterable, Any, Dict
from base.models import User


class UserListApi:
    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        username = serializers.CharField()
        email = serializers.CharField()

    def get(self, request: Request) -> Response:
        users: Iterable[User] = user_list()

        #TODO type
        serializer = self.OutputSerializer(users, many=True).data

        return Response(serializer)


class UserDetailApi:
    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        username = serializers.CharField()
        email = serializers.CharField()

    def get(self, request: Request, user_id: int) -> Response:
        user: User = user_get(id=user_id)

        #TODO type
        serializer = self.OutputSerializer(user).data

        return Response(serializer)


class UserCreateApi:
    class InputSerializer(serializers.Serializer):
        username = serializers.CharField()
        email = serializers.CharField()
        password = serializers.CharField()

    def post(self, request: Request) -> Response:
        serializer = self.InputSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)

        user_create(**serializer)

        return Response(status.HTTP_201_CREATED)
    

class UserUpdateApi:
    class InputSerializer(serializers.Serializer):
        username = serializers.CharField(required=False)
        email = serializers.CharField(required=False)
        password = serializers.CharField(required=False)

    def put(self, request: Request, user_id: int) -> Response:
        serializer = self.InputSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)

        data: Dict[str, str] = serializer.validated_data

        user_update(id=user_id, data=data)

        return Response(status.HTTP_200_OK)
    

class UserDeleteApi:
    def delete(self, request: Request, user_id: int):
        serializer = self.InputSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)

        data: Dict[str, str] = serializer.validated_data

        user_delete(id=user_id)

        return Response(status.HTTP_200_OK)
