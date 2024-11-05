from django.urls import path

from .views import index, show_organization

app_name = "frontend"

urlpatterns = [
    path("", index, name="home"),
    path("organization/<int:org_id>", show_organization, name="organization"),

]
