from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView, DetailView


from apps.device.models import Organization, Device, Verification
from apps.frontend.servises.db_services import (
    get_filter_organization,
    get_metering_units,
    get_devices,
    get_customers,
)
from .forms import UploadFileForm, DeviceVerificationFormset
from .mixins import DataMixin
from .servises.file_services import handle_uploaded_file
from .tasks import download_device_from_file_into_db, refresh_valid_date


class IndexView(DataMixin, LoginRequiredMixin, TemplateView, FormView):
    template_name = "frontend/index.html"
    title_page = "Главная страница"

    # TODO: сделать форму для загрузки файла через HTMX
    form_class = UploadFileForm
    success_url = reverse_lazy("frontend:home")

    def form_valid(self, form):
        files = form.cleaned_data["file_field"]
        for f in files:
            handle_uploaded_file(f)
            download_device_from_file_into_db.delay(f.name, self.request.user.id)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        org_selected = self.request.GET.get("organization", "all")
        tso_selected = self.request.GET.get("tso", "all")
        cust_selected = self.request.GET.get("customer", "all")
        mu_selected = self.request.GET.get("metering_unit", "all")
        # dev_selected = self.request.GET.get("device", "all")

        all_user_orgs = Organization.objects.only("name", "slug").filter(
            user_to_org__user=self.request.user
        )
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["verifications"] = (
            Verification.objects.filter(device=self.object)
            .filter(is_published=True)
            .order_by("-is_actual", "-verification_date")
        )
        return context


def device_verifications_update_view(request, pk):
    """Edit children and their addresses for a single parent."""

    device = get_object_or_404(Device, id=pk)

    if request.method == 'POST':
        formset = DeviceVerificationFormset(request.POST, instance=device)
        if formset.is_valid():
            formset.save()
            return redirect('frontend:detail_device', pk=device.id)
    else:
        formset =DeviceVerificationFormset(instance=device)

    return render(request, 'frontend/includes/modal_device_verifications_update.html', {
        'device': device,
        'formset': formset})


def refresh_valid_date_view(request):
    refresh_valid_date.delay()
    return redirect("frontend:home")
