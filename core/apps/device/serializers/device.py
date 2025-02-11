from rest_framework import serializers

from .baseserializers import MySerializer
from apps.device.models import (
    InstallationPoint,
    RegistryNumber,
    TypeName,
    Device,
    Verification,
    TypeRegistry,
)


class DeviceInstallationPointSerializer(MySerializer):
    class Meta:
        model = InstallationPoint
        fields = "id", "name"


class DeviceRegistryNumberSerializer(MySerializer):
    class Meta:
        model = RegistryNumber
        fields = "id", "registry_number"


class DeviceTypeSerializer(MySerializer):
    class Meta:
        model = TypeName
        fields = "id", "type"


# class DeviceModSerializer(MySerializer):
#     class Meta:
#         model = Modification
#         fields = "id", "mod"


class TypeToRegistrySerializer(MySerializer):
    numbers_registry = serializers.CharField(required=False)

    class Meta:
        model = TypeRegistry
        fields = "id", "type", "numbers_registry"


class DeviceSerializer(MySerializer):

    registry_number = DeviceRegistryNumberSerializer(required=False)
    type = DeviceTypeSerializer(required=False)
    # mod = DeviceModSerializer(required=False)
    nodes = serializers.CharField(required=False)

    class Meta:
        model = Device
        fields = (
            "id",
            "metering_unit",
            "installation_point",
            "registry_number",
            "type",
            # "mod",
            "type_of_file",
            "factory_number",
            "nodes",
        )


class DeviceVerificationSerializer(MySerializer):
    # device = DeviceSerializer()
    organization = serializers.CharField(required=False)
    verification_date = serializers.DateField(required=False)
    is_actual = serializers.BooleanField(required=False)
    is_delete = serializers.BooleanField(required=False)

    class Meta:
        model = Verification
        fields = (
            "id",
            "device",
            "organization",
            "verification_date",
            "valid_date",
            "is_actual",
            "is_delete",
        )
