from rest_framework.views import APIView
from rest_framework import serializers, status
from rest_framework.response import Response

from rentals.services import rental_start, rental_finish, rental_update, rental_delete
from rentals.selectors import rental_list, rental_get
from utils.permissions import AdminPermissionMixin, EligiblePermissionMixin
from rentals.api.serializers import (
    RentalSerializer,
    RentalQueryParamsSerializer,
    RentalFinishSerializer,
    RentalUpdateSerializer,
)

class RentalListAPI(AdminPermissionMixin, APIView):
    serializer_class = RentalSerializer
    query_serializer = RentalQueryParamsSerializer

    def get(self, request):
        params = self.query_serializer(data=request.query_params)
        params.is_valid(raise_exception=True)
        rentals = rental_list(params=params.validated_data)
        serializer = self.serializer_class(rentals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class RentalDetailAPI(AdminPermissionMixin, APIView):
    serializer_class = RentalSerializer

    def get(self, request, rental_id):
        rental = rental_get(rental_id=rental_id)

        serializer = self.serializer_class(rental)

        return Response(serializer.data, status=status.HTTP_200_OK)

class RentalStartAPI(EligiblePermissionMixin ,APIView):
    class InputSerializer(serializers.Serializer):
        bike = serializers.IntegerField()

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        bike_id = serializer.validated_data['bike']
        user_id = request.user.id

        rental_start(user_id=user_id, bike_id=bike_id)
        
        return Response(status=status.HTTP_200_OK)

class RentalFinishAPI(EligiblePermissionMixin, APIView):
    serializer_class = RentalFinishSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = request.user.id

        rental_finish(user_id=user_id, **serializer.validated_data)

        return Response(status=status.HTTP_200_OK)


class RentalUpdateAPI(APIView):
    serializer_class = RentalUpdateSerializer

    def put(self, request, rental_id):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        rental_update(rental_id=rental_id, data=serializer.validated_data)

        return Response(status=status.HTTP_200_OK)

class RentalDeleteAPI(AdminPermissionMixin, APIView):
    def delete(self, request, rental_id):
        rental_delete(rental_id=rental_id)

        return Response(status=status.HTTP_200_OK)