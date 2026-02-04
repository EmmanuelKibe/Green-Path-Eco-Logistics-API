from django.contrib import admin
from .models import Vehicle, Shipment, Company, Profile

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    # What to show in the list view
    list_display = ('id', 'name', 'emission_factor', 'vehicle_type_display')
    search_fields = ('name',)

    # A custom method to show the description better
    def vehicle_type_display(self, obj):
        return obj.name.split()[0] # Just a helper for the UI

@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'company', 'origin', 'destination', 'carbon_footprint', 'created_at')
    list_filter = ('created_at', 'vehicle')
    # Make carbon_footprint read-only in admin since it's calculated automatically
    readonly_fields = ('carbon_footprint',)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    # What columns to show in the list view
    list_display = ('name', 'registration_number', 'created_at', 'employee_count')
    search_fields = ('name', 'registration_number')
    readonly_fields = ('registration_number', 'created_at')

    # A custom method to show how many people work for this company
    def employee_count(self, obj):
        return obj.employees.count()
    employee_count.short_description = "Number of Employees"

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'company', 'phone_number')
    list_filter = ('role', 'company') # Sidebar filters
    search_fields = ('user__username', 'user__email', 'phone_number')
    
    # Allows you to edit the role directly from the list view
    list_editable = ('role', 'company')