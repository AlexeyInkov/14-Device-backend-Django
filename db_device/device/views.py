from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet

from device.mixins import CreateModelViewSetMixin
from device.models import (
    Device,
    DeviceInstallationPoint,
    DeviceRegistryNumber,
    DeviceType,
    DeviceMod,
    TypeToRegistry,
    DeviceVerification,
)
from device.serializers import (
    DeviceSerializer,
    DeviceInstallationPointSerializer,
    DeviceRegistryNumberSerializer,
    DeviceTypeSerializer,
    DeviceModSerializer,
    TypeToRegistrySerializer,
    DeviceVerificationSerializer,
)


class DeviceViewSet(CreateModelViewSetMixin, ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class DeviceInstallationPointViewSet(CreateModelViewSetMixin, ModelViewSet):
    queryset = DeviceInstallationPoint.objects.all()
    serializer_class = DeviceInstallationPointSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class DeviceRegistryNumberViewSet(CreateModelViewSetMixin, ModelViewSet):
    queryset = DeviceRegistryNumber.objects.all()
    serializer_class = DeviceRegistryNumberSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class DeviceTypeViewSet(CreateModelViewSetMixin, ModelViewSet):
    queryset = DeviceType.objects.all()
    serializer_class = DeviceTypeSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class DeviceModViewSet(CreateModelViewSetMixin, ModelViewSet):
    queryset = DeviceMod.objects.all()
    serializer_class = DeviceModSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class TypeToRegistryViewSet(CreateModelViewSetMixin, ModelViewSet):
    queryset = TypeToRegistry.objects.all()
    serializer_class = TypeToRegistrySerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class DeviceVerificationViewSet(CreateModelViewSetMixin, ModelViewSet):
    queryset = DeviceVerification.objects.all()
    serializer_class = DeviceVerificationSerializer
    permission_classes = []
