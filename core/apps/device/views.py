from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet

from apps.device.mixins import CreateModelViewSetMixin
from apps.device.models import (
    # metering_unit
    Organization,
    UserToOrganization,
    Address,
    MeteringUnit,
    Region,
    TypeStreet,
    Street,
    # device
    Device,
    InstallationPoint,
    RegistryNumber,
    TypeName,
    # Modification,
    TypeRegistry,
    Verification,
)
from .serializers import (
    DeviceSerializer,
    DeviceInstallationPointSerializer,
    DeviceRegistryNumberSerializer,
    DeviceTypeSerializer,
    # DeviceModSerializer,
    TypeToRegistrySerializer,
    DeviceVerificationSerializer,
)
from .serializers import (
    OrganizationSerializer,
    UserToOrganizationSerializer,
    AddressSerializer,
    MeteringUnitSerializer,
    RegionSerializer,
    TypeStreetSerializer,
    StreetSerializer,
)


class OrganizationViewSet(CreateModelViewSetMixin, ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class UserToOrganizationViewSet(CreateModelViewSetMixin, ModelViewSet):
    queryset = UserToOrganization.objects.all()
    serializer_class = UserToOrganizationSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class RegionViewSet(CreateModelViewSetMixin, ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class TypeStreetViewSet(CreateModelViewSetMixin, ModelViewSet):
    queryset = TypeStreet.objects.all()
    serializer_class = TypeStreetSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class StreetViewSet(CreateModelViewSetMixin, ModelViewSet):
    queryset = Street.objects.all()
    serializer_class = StreetSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class AddressViewSet(CreateModelViewSetMixin, ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class MeteringUnitViewSet(CreateModelViewSetMixin, ModelViewSet):
    queryset = MeteringUnit.objects.all()
    serializer_class = MeteringUnitSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class DeviceViewSet(CreateModelViewSetMixin, ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class DeviceInstallationPointViewSet(CreateModelViewSetMixin, ModelViewSet):
    queryset = InstallationPoint.objects.all()
    serializer_class = DeviceInstallationPointSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class DeviceRegistryNumberViewSet(CreateModelViewSetMixin, ModelViewSet):
    queryset = RegistryNumber.objects.all()
    serializer_class = DeviceRegistryNumberSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class DeviceTypeViewSet(CreateModelViewSetMixin, ModelViewSet):
    queryset = TypeName.objects.all()
    serializer_class = DeviceTypeSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


# class DeviceModViewSet(CreateModelViewSetMixin, ModelViewSet):
#     queryset = Modification.objects.all()
#     serializer_class = DeviceModSerializer
#     permission_classes = [IsAuthenticated, IsAdminUser]


class TypeToRegistryViewSet(CreateModelViewSetMixin, ModelViewSet):
    queryset = TypeRegistry.objects.all()
    serializer_class = TypeToRegistrySerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class DeviceVerificationViewSet(CreateModelViewSetMixin, ModelViewSet):
    queryset = Verification.objects.all()
    serializer_class = DeviceVerificationSerializer
    permission_classes = []
