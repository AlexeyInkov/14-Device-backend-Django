from django.urls import path, include
from rest_framework import routers

from .views import (
    OrganizationViewSet,
    UserToOrganizationViewSet,
    RegionViewSet,
    TypeStreetViewSet,
    StreetViewSet,
    AddressViewSet,
    MeteringUnitViewSet,
)

app_name = "metering_unit"

router = routers.DefaultRouter()
router.register(r"m_unit", MeteringUnitViewSet, basename="m_unit")
router.register(r"organization", OrganizationViewSet, basename="organization")
router.register(
    r"user_to_organization", UserToOrganizationViewSet, basename="user_to_organization"
)
router.register(r"region", RegionViewSet, basename="region")
router.register(r"type_street", TypeStreetViewSet, basename="type_street")
router.register(r"street", StreetViewSet, basename="street")
router.register(r"address", AddressViewSet, basename="address")

urlpatterns = [
    path("", include(router.urls)),
]
