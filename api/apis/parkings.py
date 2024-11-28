from rest_framework.response import Response # type: ignore
from rest_framework.request import Request # type: ignore
from rest_framework import serializers, status # type: ignore
from rest_framework.views import APIView # type: ignore
from base.selectors import parking_list, parking_get
from base.services import parking_create, parking_update, parking_delete
from typing import Dict, Any

class ParkingListApi(APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name = serializers.CharField()
        coords = serializers.FloatField()

    def get(self, request: Request) -> Response:
        parkings = parking_list()

        serializer = self.OutputSerializer(parkings, many=True).data

        return Response(serializer)
    
class ParkingDetailApi(APIView):
    class OutputSerializer(serializers.Serializer):
        name = serializers.CharField()
        coords = serializers.FloatField()
    
    def get(self, request: Request, parking_id: int) -> Response:
        parking = parking_get(id=parking_id)

        serializer = self.OutputSerializer(parking, many=True).data

        return Response(serializer)

class ParkingCreateApi(APIView):
    class InputSerializer(serializers.Serializer):
        name = serializers.CharField()
        coords = serializers.FloatField()

    def post(self, request: Request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        parking_create(**serializer.validated_data)

        return Response(status=status.HTTP_201_CREATED)
    
class ParkingUpdateApi(APIView):
    class InputSerializer(serializers.Serializer):
        name = serializers.CharField(required=False)
        coords = serializers.CharField(required=False)

    def post(self, request: Request, parking_id: int):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data: Dict[str, Any] = serializer.validated_data
        
        parking_update(id=parking_id, data=data)

        return Response(status=status.HTTP_200_OK)

class ParkingDeleteApi(APIView):
    def delete(self, request: Request, parking_id: int):
        parking_delete(id=parking_id)

        return Response(status=status.HTTP_200_OK)
