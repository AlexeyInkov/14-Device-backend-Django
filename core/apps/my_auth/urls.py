from django.urls import path

from .views import (
    UserRegisterAPIView,
    UserLoginAPIView,
    UserLogoutAPIView,
    UserMeAPIView,
    LoginUserView,
    RegisterUserView,
    MyLogoutView,
)

app_name = "my_auth"

urlpatterns = [
    path("api/register/", UserRegisterAPIView.as_view(), name="api-register"),
    path("api/login/", UserLoginAPIView.as_view(), name="api-login"),
    path("api/logout/", UserLogoutAPIView.as_view(), name="api-logout"),
    path("me/", UserMeAPIView.as_view(), name="api-me"),
    path("register/", RegisterUserView.as_view(), name="register"),
    path("login/", LoginUserView.as_view(), name="login"),
    path("logout/", MyLogoutView.as_view(), name="logout"),
]
