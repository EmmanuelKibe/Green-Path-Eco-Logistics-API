from rest_framework import serializers
from .models import Vehicle, Shipment

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'

class ShipmentSerializer(serializers.ModelSerializer):
    # We make these read-only because the backend calculates them
    distance = serializers.ReadOnlyField()
    carbon_footprint = serializers.ReadOnlyField()

    class Meta:
        model = Shipment
        fields = [
            'id', 'origin', 'destination', 'weight', 
            'vehicle', 'distance', 'carbon_footprint', 'created_at'
        ]