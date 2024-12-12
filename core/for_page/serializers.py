from django.contrib.auth.models import User
from rest_framework import serializers

from metering_unit.serializers import OrganizationSerializer
from device.baseserializers import MySerializer
from device.models import (
    Device,
    DeviceVerification,
)
from metering_unit.models import MeteringUnit, Organization, Address


class MenuCustomerSerializer(MySerializer):
    id = serializers.CharField(source="customer__id", read_only=True)
    name = serializers.CharField(source="customer__name", read_only=True)

    class Meta:
        model = MeteringUnit
        fields = (
            "id",
            "name",
        )


class MenuSerializer(MySerializer):
    customers = serializers.SerializerMethodField()

    def get_customers(self, obj):
        qs = (
            MeteringUnit.objects.filter(tso=obj.id)
            .values("customer__id", "customer__name")
            .distinct()
        )
        serializer = MenuCustomerSerializer(instance=qs, many=True)
        return serializer.data

    class Meta:
        model = Organization
        fields = (
            "id",
            "name",
            "customers",
        )


class MenuAddressSerializer(MySerializer):
    class Meta:
        model = Address
        fields = "region", "street", "house_number", "corp", "liter"


class AddressesSerializer(MySerializer):
    customer = serializers.CharField(source="customer.name", read_only=True)
    service_organization = serializers.CharField(
        source="service_organization.name", read_only=True
    )
    tso = serializers.CharField(source="tso.name", read_only=True)
    address = serializers.SerializerMethodField()
    itp = serializers.CharField(read_only=True)
    location = serializers.SerializerMethodField()

    def get_address(self, obj):
        address = []
        if obj.address.region:
            address.append(str(obj.address.region))
        if obj.address.street:
            address.append(str(obj.address.street))
        if obj.address.house_number:
            address.append(f"д. {str(obj.address.house_number)}")
        if obj.address.corp:
            address.append(f"корп. {str(obj.address.corp)}")
        if obj.address.liter:
            address.append(f"лит {str(obj.address.liter)}")
        return ", ".join(address)

    def get_location(self, obj):
        if obj.address.latitude and obj.address.longitude:
            return {
                "latitude": obj.address.latitude,
                "longitude": obj.address.longitude,
            }

    class Meta:
        model = MeteringUnit
        fields = (
            "id",
            "customer",
            "service_organization",
            "tso",
            "address",
            "itp",
            "location",
        )


class ShortDeviceVerificationSerializer(MySerializer):
    class Meta:
        model = DeviceVerification
        fields = (
            "id",
            "organization",
            "verification_date",
            "valid_date",
            "is_actual",
            "is_delete",
        )


class ShortDeviceSerializer(MySerializer):
    installation_point = serializers.CharField(
        source="installation_point.name", read_only=True
    )

    type_of_file = serializers.CharField(
        source="type_of_file.device_type_file", read_only=True
    )

    factory_number = serializers.CharField(read_only=True)
    verification = ShortDeviceVerificationSerializer(
        source="verifications",
        many=True,
        read_only=True,
    )
    nodes = serializers.CharField(read_only=True)

    class Meta:
        model = Device
        fields = (
            "id",
            "installation_point",
            "type_of_file",
            "factory_number",
            "verification",
            "nodes",
        )
