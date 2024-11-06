from django.urls import path

from .views import index, show_tso, show_customers, show_metering_units, show_devices

app_name = "frontend"

urlpatterns = [
    path("", index, name="home"),
    path("devices/tso=<int:tso_id>/", show_tso, name="tso"),
    path("devices/tso=<int:tso_id>/customer=<int:customer_id>/", show_customers, name="customers"),
    path("devices/tso=<int:tso_id>/customer=<int:customer_id>/meterung_unit=<int:mu_id>/", show_metering_units, name="metering_units"),
    path("devices/tso=<int:tso_id>/customer=<int:customer_id>/meterung_unit=<int:mu_id>/device=<int:dev_id>", show_devices, name="devices"),

]
