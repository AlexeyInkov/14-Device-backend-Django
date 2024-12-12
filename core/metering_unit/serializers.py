from rest_framework import serializers

from .baseserializers import MySerializer
from .models import (
    UserToOrganization,
    Organization,
    Address,
    MeteringUnit,
    Street,
    TypeStreet,
    Region,
)


class UserToOrganizationSerializer(MySerializer):
    class Meta:
        model = UserToOrganization
        fields = "id", "user", "organization"


class OrganizationSerializer(MySerializer):
    class Meta:
        model = Organization
        fields = "id", "name"


class RegionSerializer(MySerializer):
    class Meta:
        model = Region
        fields = "id", "name"


class TypeStreetSerializer(MySerializer):
    class Meta:
        model = TypeStreet
        fields = "id", "name"


class StreetSerializer(MySerializer):
    type_street = serializers.PrimaryKeyRelatedField(
        queryset=TypeStreet.objects.all(), many=False, required=False
    )

    class Meta:
        model = Street
        fields = "id", "name", "type_street"


class AddressSerializer(MySerializer):
    class Meta:
        model = Address
        fields = "__all__"


class MeteringUnitSerializer(MySerializer):
    class Meta:
        model = MeteringUnit
        fields = "__all__"
