from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from .forms import LoginUserForm, RegisterUserForm
from .mixins import DataMixin
from .services import get_organizations, get_metering_units, get_devices


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

        org_selected = self.request.GET.get("org_select", "all")
        tso_selected = self.request.GET.get("tso", "all")
        cust_selected = self.request.GET.get("customer", "all")
        mu_selected = self.request.GET.get("metering_unit", "all")
        dev_selected = self.request.GET.get("device", "all")

        orgs = get_organizations(org_selected, self.request.user)

        filter_metering_units, metering_units = get_metering_units(
            tso_selected, cust_selected, orgs
        )

        devices = get_devices(mu_selected, filter_metering_units)

        tso_s = orgs.filter(pk__in=(metering_units.values("tso").distinct()))

        filters = {}
        if tso_selected != "all":
            filters["tso"] = tso_selected
        customers = orgs.filter(
            id__in=(metering_units.filter(**filters).values("customer").distinct())
        )

        context = {
            "orgs": orgs,
            "tso_s": tso_s,
            "customers": customers,
            "metering_units": filter_metering_units,
            "devices": devices,
            "org_selected": org_selected,
            "tso_selected": tso_selected,
            "cust_selected": cust_selected,
            "mu_selected": mu_selected,
            "dev_selected": dev_selected,
        }

        return context
