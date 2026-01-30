from rest_framework import serializers
from .models import Vehicle, Shipment

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

    def validate_weight(self, value):
        #Check that the weight is a positive number.
        if value <= 0:
            raise serializers.ValidationError({"Weight must be greater than zero."})
        return value

    def validate(self, data):
        #Check that origin and destination are not the same.
        if data['origin'].lower() == data['destination'].lower():
            raise serializers.ValidationError({
                "destination": "Origin and destination cannot be the same city."
            })
        return data