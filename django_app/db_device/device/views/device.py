from rest_framework.viewsets import ModelViewSet

from ..mixins.create_model_viewset import CreateModelViewSetMixin
from ..models import (
    # Device,
    # DeviceInstallationPoint,
    # DeviceRegistryNumber,
    # DeviceType,
    # DeviceMod,
    TypeToRegistry,
    DeviceVerification,
)
from device.serializers import (
    # DeviceSerializer,
    # DeviceInstallationPointSerializer,
    # DeviceRegistryNumberSerializer,
    # DeviceTypeSerializer,
    # DeviceModSerializer,
    TypeToRegistrySerializer,
    ShortDeviceVerificationSerializer,
)


# class DeviceViewSet(CreateModelViewSetMixin, ModelViewSet):
#     queryset = Device.objects.all()
#     serializer_class = DeviceSerializer
#     permission_classes = []
#
#
# class DeviceInstallationPointViewSet(CreateModelViewSetMixin, ModelViewSet):
#     queryset = DeviceInstallationPoint.objects.all()
#     serializer_class = DeviceInstallationPointSerializer
#     permission_classes = []
#
#
# class DeviceRegistryNumberViewSet(CreateModelViewSetMixin, ModelViewSet):
#     queryset = DeviceRegistryNumber.objects.all()
#     serializer_class = DeviceRegistryNumberSerializer
#     permission_classes = []
#
#
# class DeviceTypeViewSet(CreateModelViewSetMixin, ModelViewSet):
#     queryset = DeviceType.objects.all()
#     serializer_class = DeviceTypeSerializer
#     permission_classes = []
#
#
# class DeviceModViewSet(CreateModelViewSetMixin, ModelViewSet):
#     queryset = DeviceMod.objects.all()
#     serializer_class = DeviceModSerializer
#     permission_classes = []


class TypeToRegistryViewSet(CreateModelViewSetMixin, ModelViewSet):
    queryset = TypeToRegistry.objects.all()
    serializer_class = TypeToRegistrySerializer
    permission_classes = []


class DeviceVerificationViewSet(CreateModelViewSetMixin, ModelViewSet):
    queryset = DeviceVerification.objects.all()
    serializer_class = ShortDeviceVerificationSerializer
    permission_classes = []
