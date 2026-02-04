from rest_framework import generics, filters, permissions, views, status
from .models import Vehicle, Shipment
from .serializers import VehicleSerializer, ShipmentSerializer, RegisterSerializer, CompanyRegisterSerializer, AddEmployeeSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsOwnerOrReadOnly
from rest_framework.response import Response
from django.contrib.auth.models import User

# Registration View
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,) # Anyone can sign up
    serializer_class = RegisterSerializer

# User Profile View 
class UserProfileView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        return Response({
            "username": request.user.username,
            "email": request.user.email
        })


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
        user = self.request.user
        profile = user.profile

        # Manager: Sees EVERYTHING for Jumia
        if profile.role == 'manager':
            return Shipment.objects.filter(company=profile.company)

        # Driver: Sees only shipments assigned to him
        if profile.role == 'driver':
            return Shipment.objects.filter(company=profile.company, owner=user)

        # Client: Sees only his own shipments
        return Shipment.objects.filter(owner=user, company__isnull=True)

    def perform_create(self, serializer):
        #Read the company from user's profile
        user_company = self.request.user.profile.company

        #save the shipment with that company automatically
        serializer.save(company=user_company, owner=self.request.user)

class ShipmentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

# Company Registration View
class RegisterCompanyView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = CompanyRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Company and Manager registered!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Add Employee View
class AddEmployeeView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # SECURITY: Only managers can add employees
        if request.user.profile.role != 'manager':
            return Response({"error": "Only managers can add employees."}, status=403)

        serializer = AddEmployeeSerializer(data=request.data)
        if serializer.is_valid():
            # Create user
            user = User.objects.create_user(
                username=serializer.validated_data['username'],
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password']
            )
            # Link to the Manager's company
            profile = user.profile
            profile.company = request.user.profile.company
            profile.role = serializer.validated_data['role']
            profile.save()
            
            return Response({"message": f"Added {user.username} to {profile.company.name}"}, status=201)
        return Response(serializer.errors, status=400)