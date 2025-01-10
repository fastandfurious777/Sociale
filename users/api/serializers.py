from rest_framework import serializers
from users.models import User
from rest_framework.validators import UniqueValidator

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'is_verified', 'is_active', 'is_admin']

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    email = serializers.EmailField(
        required=True,
        max_length=255,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True)
    confirmed_password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        if data['password'] != data['confirmed_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data
    
class UpdateSerializer(UserSerializer):
    email = serializers.EmailField(required=False)
    first_name = serializers.CharField(required=False, max_length=50)
    last_name = serializers.CharField(required=False, max_length=50)
    is_verified = serializers.BooleanField(required=False)
    is_active = serializers.BooleanField(required=False)
    is_admin = serializers.BooleanField(required=False)
    

class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)
    # TODO

