import json
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from shapely import from_geojson, errors
from parkings.models import Parking


class GeoJSONField(serializers.Field):
    def to_representation(self, value):
        try:
            return json.loads(value)
        except (ValueError, TypeError) as exc:
            raise serializers.ValidationError("Invalid JSON data provided") from exc

    def to_internal_value(self, data):
        try:
            return json.dumps(data)
        except (ValueError, TypeError) as exc:
            raise serializers.ValidationError("Invalid JSON data provided") from exc


class ParkingSerializer(serializers.ModelSerializer):
    geometry = GeoJSONField(source="area")

    class Meta:
        model = Parking
        fields = ["name", "geometry", "capacity"]


class ParkingCreateSerializer(serializers.Serializer):
    name = serializers.CharField(
        max_length=50,
        required=True,
        validators=[UniqueValidator(Parking.objects.all())],
    )
    geometry = GeoJSONField(source="area", required=True)
    capacity = serializers.IntegerField(required=False)
    is_active = serializers.BooleanField(required=False)

    def validate(self, data: dict):
        if "capacity" in data and data.get("capacity") <= 0:
            raise serializers.ValidationError(
                {"detail": "Capacity must be greater than zero"}
            )
        return data

    def validate_geometry(self, value):
        try:
            from_geojson(value)
        except errors.GEOSException as exc:
            raise serializers.ValidationError(
                {"geometry": f"Invalid GeoJSON data provided: {exc}"}
            )
        return value


class ParkingUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50, required=False)
    geometry = GeoJSONField(source="area", required=False)
    capacity = serializers.IntegerField(required=False)
    is_active = serializers.BooleanField(required=False)

    def validate(self, data: dict):
        if "capacity" in data and data.get("capacity") <= 0:
            raise serializers.ValidationError(
                {"capacity": "Capacity must be greater than zero"}
            )
        return data

    def validate_geometry(self, value):
        try:
            from_geojson(value)
        except errors.GEOSException as exc:
            raise serializers.ValidationError(
                {"geometry": f"Invalid GeoJSON data provided: {exc}"}
            )
        return value
