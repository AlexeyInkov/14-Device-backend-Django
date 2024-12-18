from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from device.models import Organization
from device.serializers import OrganizationSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User(username=validated_data["username"], email=validated_data["email"])
        user.set_password(validated_data["password"])
        user.save()
        return user


class UserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = (
            "token",
            "user",
        )


class UserOrganizationSerializer(serializers.ModelSerializer):
    organizations = serializers.SerializerMethodField(read_only=True)
    # token = serializers.CharField(source="auth_token.key", read_only=True)

    def get_organizations(self, obj):
        qs = Organization.objects.filter(user_to_org__user=obj.id).values("id", "name")
        serializer = OrganizationSerializer(instance=qs, many=True)
        return serializer.data

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "organizations",
        )
