from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from device.models import Device
from metering_unit.models import Organization, MeteringUnit
from .forms import LoginUserForm, RegisterUserForm
from .mixins import DataMixin


class LoginUserView(LoginView):
    form_class = LoginUserForm
    template_name = "frontend/auth/login.html"
    extra_context = {"title": "Авторизация"}


class RegisterUserView(CreateView):
    form_class = RegisterUserForm
    template_name = "frontend/auth/register.html"
    extra_context = {"title": "Регистрация"}
    success_url = reverse_lazy("frontend:login")


class MyLogoutView(LogoutView):
    http_method_names = ["get", "post", "options"]

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class IndexView(DataMixin, LoginRequiredMixin, TemplateView):
    template_name = "frontend/index/index.html"
    title_page = "Главная страница"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["org_selected"] = self.request.GET.get("org-select", "all")
        context["tso_selected"] = self.request.GET.get("tso", "all")
        context["cust_selected"] = self.request.GET.get("customer", "all")
        context["mu_selected"] = self.request.GET.get("metering_unit", "all")
        context["dev_selected"] = self.request.GET.get("device", "all")
        context["verif_selected"] = self.request.GET.get("verification", "all")

        # Orgs query
        context["orgs"] = Organization.objects.only("name").filter(
            user_to_org__user=self.request.user
        )
        # Orgs filter
        if context["org_selected"] != "all":
            context["orgs"] = context["orgs"].filter(pk=context["org_selected"])
        # MeteringUnit query
        context["metering_units"] = (
            MeteringUnit.objects.only(
                "customer__name",
                "address__region__name",
                "address__region__parent_region__name",
                "address__street__type_street__name",
                "address__street__name",
                "address__house_number",
                "address__corp",
                "address__liter",
                "address__latitude",
                "address__longitude",
                "itp",
                "tso__name",
                "service_organization__name",
            )
            .select_related("address__region")
            .select_related("address__street__type_street")
            .select_related("customer")
            .select_related("tso")
        )
        # MeteringUnit filter
        filters = {}
        if context["tso_selected"] != "all":
            filters["tso"] = context["tso_selected"]
        if context["cust_selected"] != "all":
            filters["customer"] = context["cust_selected"]

        context["metering_units"] = context["metering_units"].filter(
            Q(tso__in=context["orgs"])
            | Q(customer__in=context["orgs"])
            | Q(service_organization__in=context["orgs"])
        )
        if filters:
            context["metering_units"] = context["metering_units"].filter(**filters)
        # TSO filter
        context["tso_s"] = context["orgs"].filter(
            pk__in=(context["metering_units"].values("tso").distinct())
        )
        filters = {}
        if context["tso_selected"] != "all":
            filters["tso"] = context["tso_selected"]
        # Customer filter
        context["customers"] = context["orgs"].filter(
            id__in=(
                context["metering_units"]
                .filter(**filters)
                .values("customer")
                .distinct()
            )
        )
        # Device query
        context["devices"] = (
            Device.objects.only(
                "installation_point__name",
                "registry_number__registry_number",
                "type__type",
                "mod__mod",
                "type_of_file__device_type_file",
                "type_of_file__numbers_registry",
                "factory_number",
                "notes",
            )
            .select_related("type_of_file")
            .select_related("installation_point")
            .prefetch_related("verifications")
        )
        # Device filter
        if context["mu_selected"] and context["mu_selected"] != "all":
            context["devices"] = context["devices"].filter(
                metering_unit__in=[context["mu_selected"]]
            )
        else:
            context["devices"] = context["devices"].filter(
                metering_unit__in=context["metering_units"].values_list("pk", flat=True)
            )

        return context
