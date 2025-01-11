from users.selectors import user_list, user_get, user_get_by_email
from users.services import user_create, user_update, user_delete
from .serializers import UserSerializer, LoginSerializer, RegisterSerializer, UpdateSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions, authentication
from django.contrib.auth import login
from rest_framework.throttling import UserRateThrottle


class LoginThrottle(UserRateThrottle):
    rate = '5/min'

class AdminPermissionMixin:
    """Mixin to enforce admin  only access and session auth"""
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAdminUser]


class UserLoginApi(APIView):
    serializer_class = LoginSerializer
    throttle_classes = [LoginThrottle]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = user_get_by_email(email=data['email'])
        if user is None or not user.check_password(data['password']) or not user.is_eligible:
            return Response(
            {"detail": "Invalid credentials"},
            status=status.HTTP_400_BAD_REQUEST
            )
       

        login(request, user)
        return Response(
            {"detail": "Successfully logged in"},
            status=status.HTTP_200_OK
        )
        

class UserRegisterApi(APIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = user_create(**serializer.validated_data)
        
        return Response({"detail": "Account created. Please verify your email."}, status=status.HTTP_201_CREATED)
        
class UserListApi(AdminPermissionMixin, APIView):
    serializer_class = UserSerializer

    def get(self, request):
        users = user_list()
        serializer = self.serializer_class(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDetailApi(AdminPermissionMixin, APIView):
    serializer_class = UserSerializer

    def get(self, request, user_id):
        user = user_get(user_id=user_id)
        if user is None:
            return Response(
                {"detail": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserUpdateApi(AdminPermissionMixin, APIView):
    serializer_class = UpdateSerializer

    def put(self, request, user_id: int):
        serializer = self.serializer_class(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        user = user_update(user_id=user_id, data=serializer.validated_data)
        if user is not None:
            return Response({"detail": "Updated successfully"}, status=status.HTTP_200_OK)
        return Response(
            {"detail": "Update failed"},
            status=status.HTTP_404_NOT_FOUND
        )


class UserDeleteApi(AdminPermissionMixin, APIView):
    def delete(self, request, user_id: int):
        if not user_get(user_id=user_id):
            return Response(
                {"detail": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        user_delete(user_id=user_id)
        return Response(status=status.HTTP_204_NO_CONTENT)