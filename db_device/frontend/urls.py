from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import (index, show_tso, show_customers, show_metering_units, show_devices, LoginUserView, RegisterUserView)

app_name = "frontend"

urlpatterns = [
    path("", index, name="home"),
    path("register/", RegisterUserView.as_view(), name="login"),
    path("login/", LoginUserView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("devices/tso=<int:tso_id>/", show_tso, name="tso"),
    path("devices/tso=<int:tso_id>/customer=<int:customer_id>/", show_customers, name="customers"),
    path("devices/tso=<int:tso_id>/customer=<int:customer_id>/meterung_unit=<int:mu_id>/", show_metering_units, name="metering_units"),
    path("devices/tso=<int:tso_id>/customer=<int:customer_id>/meterung_unit=<int:mu_id>/device=<int:dev_id>", show_devices, name="devices"),

]
