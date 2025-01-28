from django.urls import path

from config.settings import LOGIN_URL
from .views import (
    IndexView,
    DeviceDetailView,
)
from ..my_auth.views import LoginUserView, RegisterUserView, MyLogoutView

app_name = "frontend"

urlpatterns = [

    path("", IndexView.as_view(), name="home"),
    path("device/<int:pk>/", DeviceDetailView.as_view(), name="detail_device"),

]
