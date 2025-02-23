from . serializers import ParkingSerializer, ParkingCreateSerializer, ParkingUpdateSerializer
from rest_framework.views import APIView
from rest_framework import permissions, authentication, status
from rest_framework.response import Response
from django.http import Http404
from django.core.exceptions import ValidationError as DjangoValidationError
from django_rest.exceptions import ValidationError as RestValidationError

from parkings.selectors import parking_list, parking_get
from parkings.services import parking_create, parking_update, parking_delete

# GET, LIST, CREATE, UPDATE, DELETE only by admin


class AdminPermissionMixin:
    """Mixin to enforce admin only access and session auth"""
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAdminUser]

class ParkingListApi(APIView, AdminPermissionMixin):
    serializer_class = ParkingSerializer

    def get(self, request):
        parkings = parking_list()

        serializer = self.serializer_class(parkings, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ParkingDetailApi(APIView, AdminPermissionMixin):
    serializer_class = ParkingSerializer
    
    def get(self, request, parking_id) -> Response:
        try:
            parking = parking_get(id=parking_id)
        except Http404:
            return Response({"detail": "Parking not found"},  status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(parking)

        return Response(serializer.data,  status=status.HTTP_200_OK)

class ParkingCreateApi(APIView, AdminPermissionMixin):
    serializer_class = ParkingCreateSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            parking_create(**serializer.validated_data)
        except RestValidationError as rest_error:
            return Response({"detail": str(rest_error)} ,status=status.HTTP_400_BAD_REQUEST)
        except DjangoValidationError as django_error:
            return Response({"detail": str(django_error)},status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_201_CREATED)
    
class ParkingUpdateApi(APIView):
    serializer_class = ParkingUpdateSerializer

    def post(self, request, parking_id):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            parking_update(id=parking_id, data=data)
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except RestValidationError as rest_error:
            return Response({"detail": str(rest_error)} ,status=status.HTTP_400_BAD_REQUEST)
        except DjangoValidationError as django_error:
            return Response({"detail": str(django_error)},status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)

class ParkingDeleteApi(APIView):
    def delete(self, request, parking_id):
        try:
            parking_delete(id=parking_id)
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_200_OK)