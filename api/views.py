from rest_framework import generics, filters
from .models import Vehicle, Shipment
from .serializers import VehicleSerializer, ShipmentSerializer
from django_filters.rest_framework import DjangoFilterBackend


class VehicleList(generics.ListCreateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

class ShipmentList(generics.ListCreateAPIView):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # Enable filtering by specific fields
    filterset_fields = ['vehicle', 'origin', 'destination']
    
    # Enable text search across these fields
    search_fields = ['origin', 'destination', 'id']
    
    # Allow users to order results by date or carbon footprint
    ordering_fields = ['created_at', 'carbon_footprint', 'weight']
