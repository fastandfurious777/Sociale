from rest_framework import serializers
from rentals.models import Rental

class RentalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = '__all__'

class RentalQueryParamsSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=False)
    status = serializers.CharField(required=False)

    def validate_status(self, value: str):
        if value.upper() not in Rental.Status.names:
            raise serializers.ValidationError("Invalid status")
        return value.upper()

class RentalFinishSerializer(serializers.Serializer):
    lon = serializers.FloatField()
    lat = serializers.FloatField()
   
class RentalUpdateSerializer(serializers.Serializer):
    status = serializers.CharField(required=False)
    started_at = serializers.DateTimeField(required=False)
    finished_at = serializers.DateTimeField(required=False)

    def validate_status(self, value: str):
        if value.upper() not in Rental.Status.values:
            raise serializers.ValidationError("Invalid status")
    return value.upper()