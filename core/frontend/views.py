from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from metering_unit.models import Organization
from .forms import LoginUserForm, RegisterUserForm
from .mixins import DataMixin
from .db_services import (
    get_filter_organization,
    get_metering_units,
    get_devices,
    get_customers,
)


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

        org_selected = self.request.GET.get("organization", "all")
        tso_selected = self.request.GET.get("tso", "all")
        cust_selected = self.request.GET.get("customer", "all")
        mu_selected = self.request.GET.get("metering_unit", "all")
        dev_selected = self.request.GET.get("device", "all")

        all_user_orgs = Organization.objects.only("name", "slug").filter(user_to_org__user=self.request.user)
        filter_org, select_org = get_filter_organization(org_selected, all_user_orgs)

        filter_metering_units, metering_units = get_metering_units(
            tso_selected, cust_selected, filter_org
        )

        return {
            "all_user_orgs": all_user_orgs,
            "select_org": select_org,
            "tso_s": all_user_orgs.filter(
                pk__in=(metering_units.values("tso").distinct())
            ),
            "customers": get_customers(tso_selected, metering_units, all_user_orgs),
            "metering_units": filter_metering_units,
            "devices": get_devices(mu_selected, filter_metering_units),
            "org_selected": org_selected,
            "tso_selected": tso_selected,
            "cust_selected": cust_selected,
            "mu_selected": mu_selected,
            "dev_selected": dev_selected,
        }
