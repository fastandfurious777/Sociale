from rest_framework import serializers
from parkings.models import Parking
from parkings.utils import validate_polygon

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
        if "area" not in data:
            raise serializers.ValidationError({"detail": "'area' field is required."})
        
        validate_polygon(data["area"])
        return data


class ParkingUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=50, required=False)
    area = serializers.JSONField(required=False)
    capacity = serializers.IntegerField(required=False)
    is_active = serializers.BooleanField(required=False) 

    def validate(self, data: dict):
        if data.get("area"):
            validate_polygon(data["area"])
        return data
