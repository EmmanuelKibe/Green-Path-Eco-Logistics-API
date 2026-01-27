from django.urls import path
from .views import VehicleList, ShipmentList

urlpatterns = [
    path('vehicles/', VehicleList.as_view(), name='vehicle-list'),
    path('shipments/', ShipmentList.as_view(), name='shipment-list'),
]