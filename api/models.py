from django.db import models
import uuid
from django.core.validators import MinValueValidator
from .services import calculate_distance
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Company(models.Model):
    name = models.CharField(max_length=255)
    registration_number = models.CharField(
        max_length=100, 
        unique=True, 
        editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.registration_number:
            # Generates a prefix 'GP-' followed by a unique 8-character code
            self.registration_number = f"GP-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Companies"

    def __str__(self):
        return f"{self.name} ({self.registration_number})"

class Profile(models.Model):
    ROLE_CHOICES = (
        ('driver', 'Driver'),
        ('manager', 'Manager'),
        ('client', 'Client'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Every user profile must point to a Company
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True, related_name='employees')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='client')
    phone_number = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.role}) - {self.company.name if self.company else 'No Company'}"

# Create or update user profile whenever User instance is created/updated
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

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
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        User, 
        related_name='shipments', 
        on_delete=models.CASCADE,
        null=True,  # Temporarily allow null for testing
        blank=True
    )
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
        # Perform the standard save first
        is_new = self._state.adding
        super().save(*args, **kwargs)
        
        if is_new or not self.carbon_footprint:
            from .tasks import compute_shipment_metrics_task
            # In Eager mode, this line executes the task immediately
            compute_shipment_metrics_task(str(self.id))
      

    def __str__(self):
        return f"Shipment {self.id} - {self.carbon_footprint}kg CO2"

