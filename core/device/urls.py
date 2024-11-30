from django.urls import path, include
from rest_framework import routers


from .views import (
    DeviceInstallationPointViewSet,
    TypeToRegistryViewSet,
    DeviceViewSet,
    DeviceVerificationViewSet,
)

app_name = "device"

router = routers.DefaultRouter()
router.register(
    r"installation_point", DeviceInstallationPointViewSet, basename="installation_point"
)
# router.register(r"registry_number", TypeToRegistryViewSet, basename="registry_number")
# router.register(r"type", TypeToRegistryViewSet, basename="type")
# router.register(r"mod", TypeToRegistryViewSet, basename="mod")
router.register(r"dev", DeviceViewSet, basename="dev")
router.register(r"type_to_registry", TypeToRegistryViewSet, basename="type_to_registry")
router.register(
    r"device_verification", DeviceVerificationViewSet, basename="device_verification"
)


urlpatterns = [
    path("", include(router.urls)),
]
