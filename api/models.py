from django.db import models
import uuid
from django.core.validators import MinValueValidator
from .services import calculate_distance

class Vehicle(models.Model):
    """
    Lookup table for vehicle types and their specific CO2 emission factors.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    # Emission factor: kg of CO2 per ton-km
    emission_factor = models.DecimalField(
        max_length=10, 
        decimal_places=4, 
        max_digits=10,
        validators=[MinValueValidator(0.0001)]
    )
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Shipment(models.Model):
    """
    Records shipment details and automatically calculates carbon footprint.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    origin = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    
    # Positive constraints via MinValueValidator
    distance = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0.1)],
        null=True,
        blank=True  
    )
    weight = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0.1)]
    )
    
    # link to Vehicle; PROTECT ensures we don't lose data if a vehicle is deleted
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT)
    
    # Result of: distance * weight * vehicle.emission_factor
    carbon_footprint = models.DecimalField(
        max_digits=12, 
        decimal_places=3, 
        null=True, 
        blank=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # If distance isn't provided, calculate it automatically!
        if not self.distance and self.origin and self.destination:
            calculated = calculate_distance(self.origin, self.destination)
            if calculated:
                self.distance = calculated
                
        # Then do the carbon calculation
        self.carbon_footprint = float(self.distance) * float(self.weight) * float(self.vehicle.emission_factor)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Shipment {self.id} - {self.carbon_footprint}kg CO2"

