from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import (
    LoginUserView,
    RegisterUserView,
    IndexView,
)

app_name = "frontend"

urlpatterns = [
    # path("", index, name="home"),
    path("register/", RegisterUserView.as_view(), name="login"),
    path("login/", LoginUserView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("", IndexView.as_view(), name="home"),

]
