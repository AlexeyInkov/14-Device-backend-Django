from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet

from metering_unit.mixins import CreateModelViewSetMixin
from metering_unit.models import (
    Organization,
    UserToOrganization,
    Address,
    MeteringUnit,
    Region,
    TypeStreet,
    Street,
)
from metering_unit.serializers import (
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
