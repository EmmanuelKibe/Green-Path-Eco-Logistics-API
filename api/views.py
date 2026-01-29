from rest_framework import generics, filters, permissions
from .models import Vehicle, Shipment
from .serializers import VehicleSerializer, ShipmentSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsOwnerOrReadOnly


class VehicleList(generics.ListCreateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] #Can be seen publicly but only modified by staff

class ShipmentList(generics.ListCreateAPIView):
    serializer_class = ShipmentSerializer
    permission_classes = [permissions.IsAuthenticated] #Must be logged in to do anything
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # Enable filtering by specific fields
    filterset_fields = ['vehicle', 'origin', 'destination']
    
    # Enable text search across these fields
    search_fields = ['origin', 'destination', 'id']
    
    # Allow users to order results by date or carbon footprint
    ordering_fields = ['created_at', 'carbon_footprint', 'weight']

    def get_queryset(self):
        # Users only see THEIR own shipments
        return Shipment.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        # Automatically set the owner to the current logged-in user
        serializer.save(owner=self.request.user)

class ShipmentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]