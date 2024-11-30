from django.contrib.auth.models import User
from django.db.models import Prefetch
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from device.models import (
    Device,
    DeviceVerification,
)
from metering_unit.models import (
    MeteringUnit,
    Organization,
)
from .serializers import (
    MenuSerializer,
    AddressesSerializer,
    ShortDeviceSerializer,
    # UserOrganizationSerializer,
)


class MenuListAPIView(ListAPIView):
    queryset = Organization.objects.prefetch_related("mu_tso").filter(
        pk__in=MeteringUnit.objects.values_list("tso", flat=True)
    )
    serializer_class = MenuSerializer
    # permission_classes = (IsAuthenticated,)


class AddressListAPIView(ListAPIView):
    serializer_class = AddressesSerializer
    # permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = (
            MeteringUnit.objects.select_related("customer")
            .select_related("service_organization")
            .select_related("tso")
            .select_related("address")
        )
        if (
            self.request.query_params.get("customer") is not None
            and self.request.query_params.get("tso") is not None
        ):
            return queryset.filter(
                customer=self.request.query_params.get("customer"),
                tso=self.request.query_params.get("tso"),
            )
        elif self.request.query_params.get("customer") is not None:
            queryset = queryset.filter(
                customer=self.request.query_params.get("customer")
            )
        elif self.request.query_params.get("tso") is not None:
            queryset = queryset.filter(tso=self.request.query_params.get("tso"))
        return queryset


class DeviceListAPIView(ListAPIView):
    serializer_class = ShortDeviceSerializer
    # permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = (
            Device.objects
            # .select_related("registry_number__device_type_set")
            .select_related("type_of_file")
            .select_related("mod")
            .select_related("installation_point")
            .select_related("metering_unit")
            .prefetch_related(  # "verifications")
                Prefetch(
                    "verifications",
                    queryset=DeviceVerification.objects.filter(
                        is_actual=False, is_delete=False
                    ),
                )
            )
            # .filter(verifications__is_actual=True)
        )
        if self.request.query_params.get("metering_unit") is None:
            return queryset
        return queryset.filter(
            metering_unit=self.request.query_params.get("metering_unit")
        )


# class OrganizationListAPIView(ListAPIView):
#     serializer_class = UserOrganizationSerializer
#
#     def get_queryset(self):
#         queryset = User.objects.prefetch_related("user_to_org__organization")
#         if self.request.user.is_authenticated:
#             return queryset.filter(user_to_org=self.request.user.pk)
#         return None
