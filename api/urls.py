from django.urls import path
from .views import VehicleList, ShipmentList, ShipmentDetail, RegisterView, UserProfileView

urlpatterns = [
    path('vehicles/', VehicleList.as_view(), name='vehicle-list'),
    path('shipments/', ShipmentList.as_view(), name='shipment-list'),
    path('shipments/<uuid:pk>/', ShipmentDetail.as_view(), name='shipment-detail'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]