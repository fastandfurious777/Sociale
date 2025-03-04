from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from parkings.selectors import parking_list, parking_get
from parkings.services import parking_create, parking_update, parking_delete
from utils.permissions import EligiblePermissionMixin, AdminPermissionMixin
from . serializers import ParkingSerializer, ParkingCreateSerializer, ParkingUpdateSerializer

class ParkingListApi(EligiblePermissionMixin, APIView):
    serializer_class = ParkingSerializer

    def get(self, request):
        user = request.user
        include_inactive = request.query_params.get("include_inactive")

        if user.is_staff and include_inactive:
            parkings = parking_list(include_inactive=True)
        elif not user.is_staff and include_inactive:
            return Response( 
                {"detail": "Forbidden: You cannot include inactive parkings."},
                status=status.HTTP_403_FORBIDDEN
            )
        else:
            parkings = parking_list()

        serializer = self.serializer_class(parkings, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ParkingDetailApi(AdminPermissionMixin, APIView):
    serializer_class = ParkingSerializer
    
    def get(self, request, parking_id) -> Response:
        parking = parking_get(parking_id=parking_id)

        serializer = self.serializer_class(parking)

        return Response(serializer.data,  status=status.HTTP_200_OK)

class ParkingCreateApi(AdminPermissionMixin, APIView):
    serializer_class = ParkingCreateSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        parking_create(**serializer.validated_data)

        return Response(status=status.HTTP_201_CREATED)
    
class ParkingUpdateApi(AdminPermissionMixin, APIView):
    serializer_class = ParkingUpdateSerializer

    def put(self, request, parking_id):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        parking_update(parking_id=parking_id, data=data)

        return Response(status=status.HTTP_200_OK)
    
class ParkingDeleteApi(AdminPermissionMixin, APIView):
    def delete(self, request, parking_id):
        parking_delete(parking_id=parking_id)

        return Response(status=status.HTTP_200_OK)