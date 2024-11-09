from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from device.models import Device
from metering_unit.models import Organization, MeteringUnit
from .forms import LoginUserForm, RegisterUserForm
from .mixins import DataMixin


class LoginUserView(LoginView):
    form_class = LoginUserForm
    template_name = "frontend/login.html"
    extra_context = {"title": "Авторизация"}


class RegisterUserView(CreateView):
    form_class = RegisterUserForm
    template_name = "frontend/register.html"
    extra_context = {"title": "Регистрация"}
    success_url = reverse_lazy("frontend:login")


class IndexView(DataMixin, LoginRequiredMixin, TemplateView):
    template_name = "frontend/index.html"
    title_page = "Главная страница"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["orgs"] = Organization.objects.filter(
            user_to_org__user=self.request.user
        )
        context["metering_units"] = (
            MeteringUnit.objects.filter(
                Q(tso__in=context["orgs"])
                | Q(customer__in=context["orgs"])
                | Q(service_organization__in=context["orgs"])
            )
            .select_related("address__region")
            .select_related("address__street__type_street")
        )

        context["devices"] = Device.objects.filter(
            metering_unit__in=context["metering_units"].values_list("pk", flat=True)
        ).select_related("type_of_file")

        context["tso_selected"] = self.request.GET.get("tso", "all")
        context["cust_selected"] = self.request.GET.get("customer", "all")
        context["mu_selected"] = self.request.GET.get("metering_unit", "all")
        context["dev_selected"] = self.request.GET.get("device", "all")
        # context["verif"] = context["devices"].filter(pk=context["dev_selected"])

        return context
