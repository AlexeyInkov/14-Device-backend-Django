from django.urls import path

from .views import (
    UserRegisterAPIView,
    UserLoginAPIView,
    UserLogoutAPIView,
)

app_name = "my_auth"

urlpatterns = [
    path("register/", UserRegisterAPIView.as_view(), name="register"),
    path("login/", UserLoginAPIView.as_view(), name="login"),
    path("logout/", UserLogoutAPIView.as_view(), name="logout"),
]
