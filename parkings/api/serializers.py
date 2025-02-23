from django_rest import serializers
from parkings.models import Parking

class ParkingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parking
        fields = ['name', 'area', 'capacity']


class ParkingCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=50, required=True)
    area = serializers.JSONField(required=True)
    capacity = serializers.IntegerField(required=False)
    is_active = serializers.BooleanField(required=False) 

    def validate(self, data):
        if "type" not in data and "coordinates" not in data: 
            raise serializers.ValidationError("Invalid GEOJSON object")
        if data["type"] != "Polygon":
            raise serializers.ValidationError("Area must be a 'Polygon' type ")
        
        return data


class ParkingUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=50, required=False)
    area = serializers.JSONField(required=False)
    capacity = serializers.IntegerField(required=False)
    is_active = serializers.BoolField(required=False) 

    def validate(self, data):
        if "type" not in data and "coordinates" not in data: 
            raise serializers.ValidationError("Invalid GEOJSON object")
        if data["type"] != "Polygon":
            raise serializers.ValidationError("Area must be a 'Polygon' type ")
        
        return data
