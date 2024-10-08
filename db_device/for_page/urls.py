from django.urls import path

from .views import (
    MenuListAPIView,
    AddressListAPIView,
    DeviceListAPIView,
    # OrganizationListAPIView,
)

app_name = "for_page"

urlpatterns = [
    path("menu/", MenuListAPIView.as_view(), name="menu"),
    path("addresses/", AddressListAPIView.as_view(), name="addresses"),
    path("devices/", DeviceListAPIView.as_view(), name="devices"),
    # path("organizations/", OrganizationListAPIView.as_view(), name="organizations"),
]
