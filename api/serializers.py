from rest_framework import serializers
from .models import Vehicle, Shipment
from django.contrib.auth.models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_password=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'

class ShipmentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    # We make these read-only because the backend calculates them
    distance = serializers.ReadOnlyField()
    carbon_footprint = serializers.ReadOnlyField()

    class Meta:
        model = Shipment
        fields = [
            'id', 'origin', 'destination', 'weight', 
            'vehicle', 'distance', 'carbon_footprint', 'owner', 'created_at'
        ]