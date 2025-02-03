from django.urls import path

from .views import (
    IndexView,
    DeviceDetailView,
    refresh_valid_date_view
)

app_name = "frontend"

urlpatterns = [

    path("", IndexView.as_view(), name="home"),
    path("device/<int:pk>/", DeviceDetailView.as_view(), name="detail_device"),
    path("refresh-valid-date/", refresh_valid_date_view, name="refresh_valid_date"),

]
