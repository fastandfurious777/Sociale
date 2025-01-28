from django.contrib.auth import login
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from rest_framework import status, permissions, authentication
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView

from users.selectors import user_list, user_get, user_get_by_email
from users.services import user_create, user_update, user_delete
from utils.emails import send_verification_email, send_password_reset_email
from .serializers import (
    UserSerializer,
    LoginSerializer,
    RegisterSerializer,
    UpdateSerializer,
    ResetPasswordRequestSerializer,
    ResetPasswordSerializer,
    VerifyEmailSerializer,
)


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
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = user_create(**serializer.validated_data)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        try:
            send_verification_email(user.email, uid, token)
        except Exception as e:
            #TODO add logger
            return Response({"detail": "Something unexpected happened."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
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

class UserCreateApi(AdminPermissionMixin, APIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_create(**serializer.validated_data)

        return Response({"detail": "Account created."}, status=status.HTTP_201_CREATED)
    
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
            status=status.HTTP_400_BAD_REQUEST
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


class VerifyEmailApi(APIView):
    serializer_class = VerifyEmailSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            user_id = int(force_str(urlsafe_base64_decode(data['uid'])))
            user = user_get(user_id=user_id)
            if user is None:
                return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND) 
        except (TypeError, ValueError, OverflowError):
            return Response({"detail": "Invalid verification data"}, status=status.HTTP_400_BAD_REQUEST)

        if default_token_generator.check_token(user, data['token']):
            user_update(user_id=user_id, data={'is_active': True})
            return Response({"detail": "Account verified successfully"},status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        

class ResetPasswordRequestApi(APIView):

    serializer_class = ResetPasswordRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        user = user_get_by_email(data['email'])
        if user is None:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        try:
            send_password_reset_email(user.email, uid, token)
        except Exception:
            # TODO Logger and specify exceptions that can happen
            return Response({"detail": "Something unexpected happened."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({"detail": "Your password reset link has been sent"}, status=status.HTTP_200_OK)


class ResetPasswordCheckApi(APIView):

    serializer_class = ResetPasswordSerializer

    def put(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        user_id = int(force_str(urlsafe_base64_decode(data['uid'])))
        user = user_get(user_id=user_id)

        if user is None:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    
        if default_token_generator.check_token(user, data['token']):
            user.set_password(data['password'])
            user.full_clean()
            user.save()
            return Response({"detail": "Your password has been changed successfully"},status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)