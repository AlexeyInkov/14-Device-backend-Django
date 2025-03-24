from django.urls import path

from .views import (
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

app_name = "frontend"

urlpatterns = [
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
        "upload-data-from-file/", upload_device_from_file_view, name="load_data_from_file"
    ),
    path("download-data-to-file/", download_device_to_file_view, name="load_data_to_file"),
]
