
from rest_framework.response import Response # type: ignore
from rest_framework.request import Request # type: ignore
from rest_framework import serializers, status # type: ignore
from rest_framework.views import APIView # type: ignore
from base.selectors import rental_list, rental_get
from base.services import rental_create, rental_update, rental_delete
from typing import Dict, Any

class RentalListApi(APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        user = serializers.IntegerField()
        bike = serializers.IntegerField()
        started_at = serializers.DateTimeField()
        finished_at = serializers.DateTimeField()
    
    def get(self, request: Request):
        rentals = rental_list()

        serializer = self.OutputSerializer(rentals, many=True).data

        return Response(serializer)

class RentalDetailApi(APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        user = serializers.IntegerField()
        bike = serializers.IntegerField()
        started_at = serializers.DateTimeField()
        finished_at = serializers.DateTimeField()
    
    def get(self, request: Request, rental_id: int):
        rentals = rental_get(id=rental_id)

        serializer = self.OutputSerializer(rentals, many=True).data

        return Response(serializer)
    
class RentalCreateApi(APIView):
    class InputSerializer(serializers.Serializer):
        user = serializers.IntegerField()
        bike = serializers.IntegerField()
        started_at = serializers.DateTimeField(required=False)
        finished_at = serializers.DateTimeField(required=False)

    def post(self, request: Request):
        serializer = self.InputSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        rental_create(**serializer.validated_data)

        return Response(status=status.HTTP_201_CREATED)

        
class RentalUpdateApi(APIView):
    class InputSerializer(serializers.Serializer):
        user = serializers.IntegerField(required=False)
        bike = serializers.IntegerField(required=False)
        started_at = serializers.DateTimeField(required=False)
        finished_at = serializers.DateTimeField(required=False)
    
    def post(self, request: Request, rental_id: int):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data: Dict[str, Any] = serializer.validated_data
        rental_update(id=rental_id, data=data)

        return Response(status=status.HTTP_200_OK)

class RentalDeleteApi(APIView):
    def delete(self, request: Request, bike_id: int):
        rental_delete(id=bike_id)

        return Response(status=status.HTTP_200_OK)
        