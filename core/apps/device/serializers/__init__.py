__all__ = [
    "MySerializer",
    # metering_unit
    "UserToOrganizationSerializer",
    "OrganizationSerializer",
    "RegionSerializer",
    "TypeStreetSerializer",
    "StreetSerializer",
    "AddressSerializer",
    "MeteringUnitSerializer",
    # device
    "DeviceInstallationPointSerializer",
    "DeviceRegistryNumberSerializer",
    "DeviceTypeSerializer",
    # "DeviceModSerializer",
    "TypeToRegistrySerializer",
    "DeviceSerializer",
    "DeviceVerificationSerializer",
]

from apps.device.serializers.device import (
    DeviceInstallationPointSerializer,
    DeviceRegistryNumberSerializer,
    DeviceTypeSerializer,
    # DeviceModSerializer,
    TypeToRegistrySerializer,
    DeviceSerializer,
    DeviceVerificationSerializer,
)
from .baseserializers import MySerializer
from .metering_unit import (
    UserToOrganizationSerializer,
    OrganizationSerializer,
    RegionSerializer,
    TypeStreetSerializer,
    StreetSerializer,
    AddressSerializer,
    MeteringUnitSerializer,
)
