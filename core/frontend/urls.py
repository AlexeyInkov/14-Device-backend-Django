from django.urls import path

from config.settings import LOGIN_URL
from .views import (
    LoginUserView,
    RegisterUserView,
    IndexView,
    MyLogoutView,
)

app_name = "frontend"

urlpatterns = [
    # path("", index, name="home"),
    path("register/", RegisterUserView.as_view(), name="login"),
    path("login/", LoginUserView.as_view(), name="login"),
    path(
        "logout/",
        MyLogoutView.as_view(next_page=LOGIN_URL),
        name="logout",
    ),
    path("", IndexView.as_view(), name="home"),
]
