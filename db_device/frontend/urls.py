from django.urls import path

from .views import index, show_tso, show_customers

app_name = "frontend"

urlpatterns = [
    path("", index, name="home"),
    path("tso/<int:tso_id>/", show_tso, name="tso"),
    path("customer/<int:tso_id>/<int:customer_id>/", show_customers, name="customers"),

]
