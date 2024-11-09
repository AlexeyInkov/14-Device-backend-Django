from django.contrib.auth.views import LogoutView
from django.urls import path, reverse_lazy

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
    path(
        "logout/",
        LogoutView.as_view(next_page=reverse_lazy("frontend:home")),
        name="logout",
    ),
    path("", IndexView.as_view(), name="home"),
]
