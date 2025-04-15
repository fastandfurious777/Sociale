from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from bikes.api.serializers import (
    BikeSerializer,
    BikeDetailSerializer,
    BikeCreateSerializer,
    BikeUpdateSerializer,
)
from bikes.selectors import bike_list, bike_get
from bikes.services import bike_create, bike_update, bike_delete
from utils.permissions import AdminPermissionMixin, EligiblePermissionMixin


class BikeListAPI(EligiblePermissionMixin, APIView):
    serializer_class = BikeSerializer

    def get(self, request):
        user = request.user
        include_unavailable = request.query_params.get("include_unavailable", False)

        if not user.is_staff and include_unavailable:
            return Response(
                {"detail": "Forbidden: You cannot include unavailable bikes"},
                status=status.HTTP_403_FORBIDDEN,
            )

        if user.is_staff and include_unavailable:
            bikes = bike_list(include_unavailable=True)
        else:
            bikes = bike_list()

        serializer = self.serializer_class(bikes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BikeDetailAPI(AdminPermissionMixin, APIView):
    serializer_class = BikeDetailSerializer

    def get(self, request, bike_id):
        bike = bike_get(bike_id=bike_id)

        serializer = self.serializer_class(bike)

        return Response(serializer.data, status=status.HTTP_200_OK)


class BikeCreateAPI(AdminPermissionMixin, APIView):
    serializer_class = BikeCreateSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        bike_create(**serializer.validated_data)

        return Response(status=status.HTTP_201_CREATED)


class BikeUpdateAPI(AdminPermissionMixin, APIView):
    serializer_class = BikeUpdateSerializer

    def put(self, request, bike_id):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        bike_update(bike_id=bike_id, data=serializer.validated_data)

        return Response(status=status.HTTP_200_OK)


class BikeDeleteAPI(AdminPermissionMixin, APIView):
    def delete(self, request, bike_id):
        bike_delete(bike_id=bike_id)

        return Response(status=status.HTTP_200_OK)
