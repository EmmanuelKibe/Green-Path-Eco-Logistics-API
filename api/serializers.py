from rest_framework import serializers
from .models import Vehicle, Shipment, Company, Profile
from django.contrib.auth.models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

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

class CompanyRegisterSerializer(serializers.Serializer):
    # Company data
    company_name = serializers.CharField(max_length=255)
    
    # User/Admin data
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        # 1. Create the Company
        company = Company.objects.create(name=validated_data['company_name'])
        
        # 2. Create the User
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        
        # 3. Update the Profile (linked via signal)
        profile = user.profile
        profile.company = company
        profile.role = 'manager'
        profile.save()
        
        return user

class AddEmployeeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=Profile.ROLE_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']

