from rest_framework import serializers
from bikes.models import Bike


class BikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bike
        fields = ["name", "lon", "lat"]


class BikeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bike
        fields = [
            "name",
            "lon",
            "lat",
            "qr_code",
            "is_available",
            "last_taken_by",
            "last_updated",
        ]


class BikeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bike
        fields = ["name", "lon", "lat", "code", "is_available", "last_taken_by"]


class BikeUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(required=False, max_length=100)
    lon = serializers.FloatField(required=False)
    lat = serializers.FloatField(required=False)
    code = serializers.FloatField(required=False)
    is_available = serializers.BooleanField(required=False)
    last_taken_by = serializers.IntegerField(required=False)
