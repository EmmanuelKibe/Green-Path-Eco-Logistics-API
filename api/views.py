from rest_framework import generics
from .models import Vehicle, Shipment
from .serializers import VehicleSerializer, ShipmentSerializer

class VehicleList(generics.ListCreateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

class ShipmentList(generics.ListCreateAPIView):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer
