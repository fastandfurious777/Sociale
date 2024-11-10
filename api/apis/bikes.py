
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.views import APIView
from bike_map.selectors import bike_list, bike_get
from bike_map.services import bike_create, bike_update, bike_delete

class BikeListApi(APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name = serializers.CharField()
        lon = serializers.FloatField()
        lat = serializers.FloatField()

    def get(self, request):
        bikes = bike_list()

        serializer = self.OutputSerializer(bikes, many=True).data

        return Response(serializer)
    
class BikeDetailApi(APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name = serializers.CharField()
        lon = serializers.FloatField()
        lat = serializers.FloatField()

    def get(self, request, bike_id):
        bike = bike_get(id=bike_id)
        if bike is not None:
            serializer = self.OutputSerializer(bike).data
            return Response(serializer)
        content = {'message': 'Bike not found'}
        return Response(content,status=status.HTTP_404_NOT_FOUND)
    
class BikeCreateApi(APIView):
    class InputSerializer(serializers.Serializer):
        name = serializers.CharField()
        lon = serializers.FloatField()
        lat = serializers.FloatField()
        is_available = serializers.BooleanField()

    def post(self, request):
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

    def post(self, request, bike_id):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        
        bike_update(id=bike_id, data=data)

        return Response(status=status.HTTP_200_OK)

class BikeDeleteApi(APIView):
    #Maby authentication?

    def delete(self, request, bike_id: int):
        bike_delete(id=bike_id)

        return Response(status=status.HTTP_200_OK)
        
"""
@csrf_exempt
def bike_management(request, id):
    if request.method == 'GET':
        bike = Bike.objects.filter(id=id).first()
        if bike is not None:
            return JsonResponse(
                {
                    'id': bike.id,
                    'name': bike.name,
                    'is_available': bike.is_available,
                    'lat':bike.lat, 'lon':bike.lon
                }, status = 200
            )
        else:
            return JsonResponse(
                {"error": "Not found"}, status = 404
            )  
    elif request.method == 'PUT':
        SUPPORTED_FIELDS = ["name","is_available", "lat", "lon", "code"]
        bike = Bike.objects.filter(id=id).first()
        data = json.loads(request.body.decode('utf-8'))
        if bike is None:
            return JsonResponse(
                {"message": "Not found"}, status = 404
            )
        for key in data:
                if key in SUPPORTED_FIELDS and data[key] is not None:
                    setattr(bike,key,data[key])
                else:
                    return JsonResponse(
                        {"message":"Bad request"}, status = 400
                    )
        bike.save()
        return JsonResponse(
            {"message":"Success"}, status = 200
        ) 
    elif request.method == 'DELETE':
        bike = Bike.objects.filter(id=id).first()
        if bike is None:
            return JsonResponse(
                {"message": "Not found"}, status = 404
            )
        bike.delete()
        return JsonResponse(
                {"message": "Success"}, status = 200
            )

"""
