from users.selectors import user_list, user_get
from users.services import user_create, user_update, user_delete
from .serializers import UserSerializer, LoginSerializer, RegisterSerializer, UpdateSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions, authentication
from django.contrib.auth import authenticate, login


class AdminPermissionMixin:
    """Mixin to enforce admin  only access and session auth"""
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAdminUser]


class UserLoginApi(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(request=request, **serializer.validated_data)
        
        if user is not None:
            login(request, user)
            return Response(
                {"TODO": "TODO"},
                status=status.HTTP_200_OK
            )
        
        return Response(
            {"detail": "Invalid credentials"},
            status=status.HTTP_400_BAD_REQUEST
        )


class UserListApi(AdminPermissionMixin, APIView):
    serializer_class = UserSerializer

    def get(self, request):
        users = user_list()
        serializer = self.serializer_class(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDetailApi(AdminPermissionMixin, APIView):
    serializer_class = UserSerializer

    def get(self, request, user_id):
        user = user_get(id=user_id)
        if user is None:
            return Response(
                {"detail": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserCreateApi(AdminPermissionMixin, APIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = user_create(**serializer.validated_data)
        
        return Response({"TODO": "TODO"}, status=status.HTTP_201_CREATED)


class UserUpdateApi(AdminPermissionMixin, APIView):
    serializer_class = UpdateSerializer

    def put(self, request, user_id: int):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = user_update(id=user_id, data=serializer.validated_data)
        
        if user is not None:
            return Response({"TODO": "TODO"},status=status.HTTP_200_OK)
        return Response(
            {"detail": "Update failed"},
            status=status.HTTP_404_NOT_FOUND
        )


class UserDeleteApi(AdminPermissionMixin, APIView):
    def delete(self, request, user_id: int):
        if user_delete(id=user_id):
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {"detail": "User not found"},
            status=status.HTTP_404_NOT_FOUND
        )
