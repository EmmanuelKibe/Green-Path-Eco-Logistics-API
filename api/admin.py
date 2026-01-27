from django.contrib import admin
from .models import Vehicle, Shipment

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    # What to show in the list view
    list_display = ('name', 'emission_factor', 'vehicle_type_display')
    search_fields = ('name',)

    # A custom method to show the description better
    def vehicle_type_display(self, obj):
        return obj.name.split()[0] # Just a helper for the UI

@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'origin', 'destination', 'carbon_footprint', 'created_at')
    list_filter = ('created_at', 'vehicle')
    # Make carbon_footprint read-only in admin since it's calculated automatically
    readonly_fields = ('carbon_footprint',)
