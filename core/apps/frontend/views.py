from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView, DetailView


from apps.device.models import Organization, Device, DeviceVerification
from apps.frontend.servises.db_services import (
    get_filter_organization,
    get_metering_units,
    get_devices,
    get_customers,
)
from .forms import UploadFileForm
from .mixins import DataMixin
from .servises.file_services import handle_uploaded_file
from .tasks import download_file_to_db


class IndexView(DataMixin, LoginRequiredMixin, TemplateView, FormView):
    template_name = "frontend/index.html"
    title_page = "Главная страница"

    form_class = UploadFileForm
    success_url = reverse_lazy("frontend:home")

    def form_valid(self, form):
        files = form.cleaned_data["file_field"]
        for f in files:
            handle_uploaded_file(f)
            download_file_to_db.delay(f.name, self.request.user.id)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        org_selected = self.request.GET.get("organization", "all")
        tso_selected = self.request.GET.get("tso", "all")
        cust_selected = self.request.GET.get("customer", "all")
        mu_selected = self.request.GET.get("metering_unit", "all")
        # dev_selected = self.request.GET.get("device", "all")

        all_user_orgs = Organization.objects.only("name", "slug").filter(user_to_org__user=self.request.user)
        filter_org, select_org = get_filter_organization(org_selected, all_user_orgs)

        filter_metering_units, metering_units = get_metering_units(
            tso_selected, cust_selected, filter_org
        )

        context.update(
            {
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
                # "dev_selected": dev_selected,
            }
        )

        return context


class DeviceDetailView(DataMixin, LoginRequiredMixin, DetailView):
    model = Device
    template_name = "frontend/includes/modal_list_verifications.html"
    title_page = "Поверки"

    # def get_queryset(self):
    #     return Device.objects.filter(pk=self.kwargs.get('device_id'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['verifications'] = Device.objects.get(pk=self.kwargs.get('pk')).verifications
        context['verifications'] = DeviceVerification.objects.filter(device=self.object).filter(is_delete=False).order_by('valid_date')
        return context
