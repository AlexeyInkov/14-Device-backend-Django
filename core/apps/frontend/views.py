from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic import TemplateView, ListView, DetailView

from apps.device.models import Device, Verification, Organization
from .forms import UploadFileForm, DeviceVerificationFormset
from .mixins import DataMixin
from .servises.db_services import GetIndexViewDataFromDB
from .servises.file_services import handle_uploaded_file
from .servises.request_services import get_org_selected, get_tso_selected, get_cust_selected, get_mu_selected
from .tasks import download_device_from_file_into_db, refresh_valid_date


class IndexView(DataMixin, LoginRequiredMixin, TemplateView):
    template_name = "frontend/index.html"
    title_page = "Главная страница"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        org_selected = get_org_selected(self.request)
        if org_selected:
            context["org_selected"] = org_selected
            select_org = Organization.objects.get(slug=org_selected),
            print(select_org[0])
            context["select_org"] = select_org[0]
        return context


class UserOrganizationsListView(DataMixin, LoginRequiredMixin, ListView):
    template_name = "frontend/user_organizations_list.html"
    title_page = "Организации пользователя"
    context_object_name = "user_orgs_for_select"

    def get_queryset(self):
        return GetIndexViewDataFromDB(user=self.request.user).orgs_for_select


@login_required
def load_file_view(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            files = form.cleaned_data["file_field"]
            for f in files:
                handle_uploaded_file(f)
                download_device_from_file_into_db.delay(f.name, request.user.id)
        return HttpResponse(status=204)
    else:
        form = UploadFileForm()
    return render(request, 'frontend/modal-load-file.html', {'form': form})


def refresh_valid_date_view(request):
    refresh_valid_date.delay()
    return redirect("frontend:home")


class MeteringUnitListView(DataMixin, LoginRequiredMixin, ListView):
    template_name = "frontend/metering_unit_list.html"
    title_page = "Узлы учета"
    context_object_name = "metering_units"

    def get_queryset(self):
        return GetIndexViewDataFromDB(
            user=self.request.user,
            org_selected=get_org_selected(self.request),
            tso_selected=get_tso_selected(self.request),
            cust_selected=get_cust_selected(self.request),
        ).metering_units


class MenuItemListView(DataMixin,LoginRequiredMixin, ListView):
    template_name = "frontend/menu_item_list.html"
    title_page = "Пункты меню"
    context_object_name = "menu_items"

    def get_queryset(self):
        return GetIndexViewDataFromDB(
            user=self.request.user,
            org_selected=get_org_selected(self.request),

        ).metering_units.values("tso__name", 'tso__slug').distinct()


class MenuItemDetailView(DataMixin, LoginRequiredMixin, ListView):
    template_name = "frontend/menu_item_detail.html"
    title_page = "Пункт меню"
    context_object_name = "menu_item"

    def get_queryset(self):
        return GetIndexViewDataFromDB(
            user=self.request.user,
            org_selected=get_org_selected(self.request),
            tso_selected=get_tso_selected(self.request),
        ).metering_units.values("customer__name", 'customer__slug').distinct()


class DeviceListView(DataMixin, LoginRequiredMixin, ListView):
    template_name = "frontend/device_list.html"
    title_page = "Приборы"
    context_object_name = "devices"

    def get_queryset(self):
        return GetIndexViewDataFromDB(
            user=self.request.user,
            org_selected=get_org_selected(self.request),
            tso_selected=get_tso_selected(self.request),
            cust_selected=get_cust_selected(self.request),
            mu_selected=get_mu_selected(self.request),
        ).devices


class DeviceDetailView(DataMixin, LoginRequiredMixin, DetailView):
    model = Device
    template_name = "frontend/device_detail_verification_list_modal.html"
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
            return redirect('frontend:device_detail', pk=device.id)
    else:
        formset = DeviceVerificationFormset(instance=device)

    return render(request, 'frontend/device_update_verification_list_modal.html', {
        'device': device,
        'formset': formset})
