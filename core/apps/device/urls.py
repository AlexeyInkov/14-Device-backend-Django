from django.urls import path, include
from rest_framework import routers

from .views import (
    # metering_unit
    MeteringUnitViewSet,
    OrganizationViewSet,
    UserToOrganizationViewSet,
    RegionViewSet,
    TypeStreetViewSet,
    StreetViewSet,
    AddressViewSet,
    # device
    DeviceInstallationPointViewSet,
    TypeToRegistryViewSet,
    DeviceViewSet,
    DeviceVerificationViewSet,
)

app_name = "device"

router = routers.DefaultRouter()

# metering_unit
router.register(r"m_unit", MeteringUnitViewSet, basename="m_unit")
router.register(r"organization", OrganizationViewSet, basename="organization")
router.register(
    r"user_to_organization", UserToOrganizationViewSet, basename="user_to_organization"
)
router.register(r"region", RegionViewSet, basename="region")
router.register(r"type_street", TypeStreetViewSet, basename="type_street")
router.register(r"street", StreetViewSet, basename="street")
router.register(r"address", AddressViewSet, basename="address")

# device
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
