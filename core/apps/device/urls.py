from django.urls import path

# from rest_framework import routers
#
# from .views.drf_views import (
#     # metering_unit
#     MeteringUnitViewSet,
#     OrganizationViewSet,
#     UserToOrganizationViewSet,
#     RegionViewSet,
#     TypeStreetViewSet,
#     StreetViewSet,
#     AddressViewSet,
#     # device
#     DeviceInstallationPointViewSet,
#     TypeToRegistryViewSet,
#     DeviceViewSet,
#     DeviceVerificationViewSet,
# )

# from .views.for_page import (
#     MenuListAPIView,
#     AddressListAPIView,
#     DeviceListAPIView,
# )
from .views.frontend import (
    IndexView,
    UserOrganizationsListView,
    upload_device_from_file_view,
    download_device_to_file_view,
    MeteringUnitListView,
    MenuItemListView,
    MenuItemDetailView,
    DeviceListView,
    DeviceDetailView,
    refresh_valid_date_view,
    device_verifications_update_view,
)

app_name = "device"

# router = routers.DefaultRouter()
#
# # metering_unit
# router.register(r"m_unit", MeteringUnitViewSet, basename="m_unit")
# router.register(r"organization", OrganizationViewSet, basename="organization")
# router.register(
#     r"user_to_organization", UserToOrganizationViewSet, basename="user_to_organization"
# )
# router.register(r"region", RegionViewSet, basename="region")
# router.register(r"type_street", TypeStreetViewSet, basename="type_street")
# router.register(r"street", StreetViewSet, basename="street")
# router.register(r"address", AddressViewSet, basename="address")
#
# # device
# router.register(
#     r"installation_point", DeviceInstallationPointViewSet, basename="installation_point"
# )
# # router.register(r"registry_number", TypeToRegistryViewSet, basename="registry_number")
# # router.register(r"type", TypeToRegistryViewSet, basename="type")
# # router.register(r"mod", TypeToRegistryViewSet, basename="mod")
# router.register(r"dev", DeviceViewSet, basename="dev")
# router.register(r"type_to_registry", TypeToRegistryViewSet, basename="type_to_registry")
# router.register(
#     r"device_verification", DeviceVerificationViewSet, basename="device_verification"
# )

urlpatterns = []

# frontend_urls
urlpatterns += [
    path("", IndexView.as_view(), name="home"),
    path(
        "user-organizations/",
        UserOrganizationsListView.as_view(),
        name="user_organization_list",
    ),
    path("metering-units/", MeteringUnitListView.as_view(), name="metering_unit_list"),
    path("menu-items/", MenuItemListView.as_view(), name="menu_item_list"),
    path("menu-item/", MenuItemDetailView.as_view(), name="menu_item"),
    path("devices/", DeviceListView.as_view(), name="device_list"),
    path("device/<int:pk>/", DeviceDetailView.as_view(), name="device_detail"),
    path(
        "device-verifications/update/<int:pk>/",
        device_verifications_update_view,
        name="update_device_verification",
    ),
    path("refresh-valid-date/", refresh_valid_date_view, name="refresh_valid_date"),
    path(
        "upload-data-from-file/",
        upload_device_from_file_view,
        name="load_data_from_file",
    ),
    path(
        "download-data-to-file/", download_device_to_file_view, name="load_data_to_file"
    ),
]

# DRF_URLS
# urlpatterns += [
#     path("", include(router.urls)),
# ]

# for_page
# urlpatterns += [
#     path("menu/", MenuListAPIView.as_view(), name="menu"),
#     path("addresses/", AddressListAPIView.as_view(), name="addresses"),
#     path("devices/", DeviceListAPIView.as_view(), name="devices"),
#     # path("organizations/", OrganizationListAPIView.as_view(), name="organizations"),
# ]
