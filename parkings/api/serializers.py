from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from parkings.models import Parking
from parkings.utils import validate_polygon


class ParkingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parking
        fields = ['name', 'area', 'capacity']


class ParkingCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50, required=True, validators=[UniqueValidator(Parking.objects.all())])
    area = serializers.JSONField(required=True)
    capacity = serializers.IntegerField(required=False)
    is_active = serializers.BooleanField(required=False) 

    def validate(self, data: dict):        
        if 'capacity' in data and data.get('capacity')<=0:
            raise serializers.ValidationError({'detail': 'Capacity must be greater than zero'})
        validate_polygon(data.get('area'))

        return data


class ParkingUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50, required=False)
    area = serializers.JSONField(required=False)
    capacity = serializers.IntegerField(required=False)
    is_active = serializers.BooleanField(required=False) 

    def validate(self, data: dict): 
        if data.get('area'):
            validate_polygon(data.get('area'))
        if 'capacity' in data and data.get('capacity')<=0:
            raise serializers.ValidationError({'detail': 'Capacity must be greater than zero'})
        
        return data
