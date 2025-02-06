from django.urls import path

from .views import IndexView, DeviceDetailView, refresh_valid_date_view, device_verifications_update_view

app_name = "frontend"

urlpatterns = [
    path("", IndexView.as_view(), name="home"),
    path("device/<int:pk>/", DeviceDetailView.as_view(), name="detail_device"),
    path("device-verifications/update/<int:pk>/", device_verifications_update_view, name="update_device_verification"),
    path("refresh-valid-date/", refresh_valid_date_view, name="refresh_valid_date"),
]
