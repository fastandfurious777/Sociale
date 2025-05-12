from django.contrib.auth import login
from django.contrib.auth.tokens import default_token_generator
from django.http import Http404
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView

from users.selectors import user_list, user_get, user_get_by_email
from users.services import user_create, user_update, user_delete
from users.api.serializers import (
    UserSerializer,
    LoginSerializer,
    RegisterSerializer,
    UpdateSerializer,
    ResetPasswordRequestSerializer,
    ResetPasswordSerializer,
    VerifyEmailSerializer,
)
from utils.emails import send_verification_email, send_password_reset_email
from utils.permissions import AdminPermissionMixin
import logging

logger = logging.getLogger(__name__)


class LoginThrottle(UserRateThrottle):
    rate = "5/min"


class UserLoginApi(APIView):
    serializer_class = LoginSerializer
    throttle_classes = [LoginThrottle]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            user = user_get_by_email(email=data["email"])
        except Http404:
            logger.error("USER NOT FOUND: %s", data["email"], extra={"request": request})
            return Response(
                {"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
            )

        if not user.check_password(data["password"]):
            logger.warning(
                "INVALID CREDENTIALS: %s", user.email, extra={"request": request}
            )
            return Response(
                {"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
            )

        if not user.is_eligible:
            logger.warning(
                "ACCOUNT NOT ACTIVE: %s", user.email, extra={"request": request}
            )
            return Response(
                {"detail": "Your account needs to be activated by an admin"},
                status=status.HTTP_403_FORBIDDEN,
            )

        login(request, user)
        logger.info("SUCCESSFUL LOGIN: %s", user.email, extra={"request": request})
        return Response({"detail": "Successfully logged in"}, status=status.HTTP_200_OK)


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
            logger.error("MAIL SENDING FAILED: %s", e, extra={"request": request})
            return Response(
                {"detail": "Mail sending failed"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        logger.info("CREATED ACCOUNT: %s", user.email, extra={"request": request})
        return Response(
            {"detail": "Account created. Please verify your email."},
            status=status.HTTP_201_CREATED,
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
        user = user_get(user_id=user_id)
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserCreateApi(AdminPermissionMixin, APIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_create(**serializer.validated_data)

        logger.info(
            "CREATED USER: %s",
            serializer.validated_data["email"],
            extra={"request": request},
        )
        return Response(status=status.HTTP_201_CREATED)


class UserUpdateApi(AdminPermissionMixin, APIView):
    serializer_class = UpdateSerializer

    def put(self, request, user_id: int):
        serializer = self.serializer_class(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        user_update(user_id=user_id, data=serializer.validated_data)

        logger.info("UPDATED USER: %d", user_id, extra={"request": request})
        return Response(status=status.HTTP_200_OK)


class UserDeleteApi(AdminPermissionMixin, APIView):
    def delete(self, request, user_id: int):
        user_delete(user_id=user_id)

        logger.info("DELETED USER: %d", user_id, extra={"request": request})
        return Response(status=status.HTTP_204_NO_CONTENT)


class VerifyEmailApi(APIView):
    serializer_class = VerifyEmailSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            user_id = int(force_str(urlsafe_base64_decode(data["uid"])))
        except (TypeError, ValueError, OverflowError):
            logger.error("UID DECODING FAILED: invalid uid", extra={"request": request})
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error("UID DECODING FAILED: %s", e, extra={"request": request})
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user = user_get(user_id=user_id)
        if default_token_generator.check_token(user, data["token"]):
            user.activate()
            logger.info("ACCOUNT VERIFIED: %s", user.email, extra={"request": request})
            return Response(
                {"detail": "Account verified successfully"}, status=status.HTTP_200_OK
            )

        logger.error("TOKEN CHECK FAILED: invalid token", extra={"request": request})
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordRequestApi(APIView):

    serializer_class = ResetPasswordRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        user = user_get_by_email(data["email"])

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        try:
            send_password_reset_email(user.email, uid, token)
        except Exception as e:
            logger.error("MAIL SENDING FAILED: %s", e, extra={"request": request})
            return Response(
                {"detail": "Mail sending failed"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        logger.info(
            "PASSWORD RESET REQUEST: %s", user.email, extra={"request": request}
        )
        import os

        return Response(
            {"detail": "Your password reset link has been sent"},
            status=status.HTTP_200_OK,
        )


class ResetPasswordCheckApi(APIView):

    serializer_class = ResetPasswordSerializer

    def put(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data


        try:
            user_id = int(force_str(urlsafe_base64_decode(data["uid"])))
        except (TypeError, ValueError, OverflowError):
            logger.error("UID DECODING FAILED: invalid uid", extra={"request": request})
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error("UID DECODING FAILED: %s", e, extra={"request": request})
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user = user_get(user_id=user_id)

        if default_token_generator.check_token(user, data["token"]):
            user.set_password(data["password"])
            user.full_clean()
            user.save()
            return Response(
                {"detail": "Your password has been changed successfully"},
                status=status.HTTP_200_OK,
            )

        logger.error("TOKEN CHECK FAILED: invalid token", extra={"request": request})
        return Response(status=status.HTTP_400_BAD_REQUEST)
