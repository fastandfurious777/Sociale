
from rest_framework.response import Response # type: ignore
from rest_framework.request import Request # type: ignore
from rest_framework import serializers, status # type: ignore
from rest_framework.views import APIView # type: ignore
from base.selectors import bike_list, bike_get
from base.services import bike_create, bike_update, bike_delete

class BikeListApi(APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name = serializers.CharField()
        lon = serializers.FloatField()
        lat = serializers.FloatField()

    def get(self, request: Request) -> Response:
        bikes = bike_list()

        serializer = self.OutputSerializer(bikes, many=True).data

        return Response(serializer)
    
class BikeDetailApi(APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name = serializers.CharField()
        lon = serializers.FloatField()
        lat = serializers.FloatField()

    def get(self, request: Request, bike_id: int):
        bike = bike_get(id=bike_id)

        serializer = self.OutputSerializer(bike).data
        
        return Response(serializer)

    
class BikeCreateApi(APIView):
    class InputSerializer(serializers.Serializer):
        name = serializers.CharField()
        lon = serializers.FloatField()
        lat = serializers.FloatField()
        is_available = serializers.BooleanField()

    def post(self, request: Request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        bike_create(**serializer.validated_data)

        return Response(status=status.HTTP_201_CREATED)
        
class BikeUpdateApi(APIView):
    class InputSerializer(serializers.Serializer):
        name = serializers.CharField(required=False)
        lon = serializers.FloatField(required=False)
        lat = serializers.FloatField(required=False)
        is_available = serializers.BooleanField(required=False)
        last_taken_by = serializers.IntegerField(required=False)

    def post(self, request: Request, bike_id: int):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        
        bike_update(id=bike_id, data=data)

        return Response(status=status.HTTP_200_OK)

class BikeDeleteApi(APIView):
    #Maby authentication?

    def delete(self, request: Request, bike_id: int):
        bike_delete(id=bike_id)

        return Response(status=status.HTTP_200_OK)