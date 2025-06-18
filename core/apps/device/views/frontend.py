import os

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, ListView, DetailView

import utils.request_query_params as request_utils
from apps.device.forms import UploadFileForm, DeviceVerificationFormset
from apps.device.mixins import ContextDataMixin, TemplateMixin
from apps.device.models import Device
from apps.device.services.device import DeviceServices
from apps.device.services.metering_unit import MeteringUnitServices
from apps.device.services.organization import OrganizationServices
from apps.device.services.verification import VerificationServices
from apps.device.tasks import (
    download_device_from_file_into_db,
    refresh_valid_date,
    create_excel_file,
)
from utils.file_utils import handle_uploaded_file


class IndexView(ContextDataMixin, LoginRequiredMixin, TemplateView):
    template_name = "device/index.html"
    title_page = "Главная страница"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        org_selected = request_utils.get_org_selected(self.request)
        if org_selected:
            context["select_org"] = OrganizationServices.get_by_slug(slug=org_selected)
        return context


class UserOrganizationsListView(TemplateMixin, LoginRequiredMixin, ListView):
    template_name = "device/user_organizations_list.html"
    title_page = "Организации пользователя"
    context_object_name = "user_orgs_for_select"

    def get_queryset(self):
        return OrganizationServices.get_by_user(user=self.request.user)


@login_required
def upload_device_from_file_view(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            files = form.cleaned_data["file_field"]
            for f in files:
                handle_uploaded_file(f)
                download_device_from_file_into_db.delay(f.name, request.user.id)
            else:
                return HttpResponse(status=200)
        return HttpResponse(status=400)
    else:
        form = UploadFileForm()
    return render(request, "device/modal-load-file.html", {"form": form})


@login_required
def download_device_to_file_view(request):
    metering_units = MeteringUnitServices.get_filter_metering_units(
        user=request.user,
        org_selected=request_utils.get_org_selected(request),
        tso_selected=request_utils.get_tso_selected(request),
        cust_selected=request_utils.get_cust_selected(request),
    )
    file_path = create_excel_file(metering_units)
    if file_path is not None and os.path.exists(file_path):
        with open(file_path, "rb") as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response["Content-Disposition"] = "inline; filename=" + os.path.basename(
                file_path
            )
            return response
    return render(
        request,
        "device/message.html",
        context={"message": "File not found", "mu": metering_units},
    )


@login_required
def refresh_valid_date_view(request):
    refresh_valid_date.delay()
    # TODO: сделать попап сообщение об успехе
    return redirect("device:home")


class MeteringUnitListView(
    TemplateMixin, ContextDataMixin, LoginRequiredMixin, ListView
):
    template_name = "device/metering_unit_list.html"
    title_page = "Узлы учета"
    context_object_name = "metering_units"

    def get_queryset(self):
        return MeteringUnitServices.get_filter_metering_units(
            user=self.request.user,
            org_selected=request_utils.get_org_selected(self.request),
            tso_selected=request_utils.get_tso_selected(self.request),
            cust_selected=request_utils.get_cust_selected(self.request),
        )


class MenuItemListView(TemplateMixin, ContextDataMixin, LoginRequiredMixin, ListView):
    template_name = "device/menu_item_list.html"
    title_page = "Пункты меню"
    context_object_name = "menu_items"

    def get_queryset(self):
        return MeteringUnitServices.get_menu_list(
            user=self.request.user,
            org_selected=request_utils.get_org_selected(self.request),
            tso_selected=request_utils.get_tso_selected(self.request),
            cust_selected=request_utils.get_cust_selected(self.request),
        )


class MenuItemDetailView(TemplateMixin, ContextDataMixin, LoginRequiredMixin, ListView):
    template_name = "device/menu_item_detail.html"
    title_page = "Пункт меню"
    context_object_name = "menu_item"

    def get_queryset(self):
        return MeteringUnitServices.get_menu_items(
            user=self.request.user,
            org_selected=request_utils.get_org_selected(self.request),
            tso_selected=request_utils.get_tso_selected(self.request),
            cust_selected=request_utils.get_cust_selected(self.request),
        )


class DeviceListView(TemplateMixin, ContextDataMixin, LoginRequiredMixin, ListView):
    template_name = "device/device_list.html"
    title_page = "Приборы"
    context_object_name = "devices"

    def get_queryset(self):
        return DeviceServices.get_devices(
            user=self.request.user,
            org_selected=request_utils.get_org_selected(self.request),
            tso_selected=request_utils.get_tso_selected(self.request),
            cust_selected=request_utils.get_cust_selected(self.request),
            mu_selected=request_utils.get_mu_selected(self.request),
        )


class DeviceDetailView(ContextDataMixin, LoginRequiredMixin, DetailView):
    model = Device
    template_name = "device/device_detail_verification_list_modal.html"
    title_page = "Поверки"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        device = self.get_object()
        context["verifications"] = VerificationServices.get_by_device(device=device)
        return context


# TODO: преобразовать в класс
@login_required
def device_verifications_update_view(request, pk):
    """Edit children and their addresses for a single parent."""

    device = DeviceServices.get(id=pk)
    if not device:
        raise Http404("No Device found matching the query")

    if request.method == "POST":
        formset = DeviceVerificationFormset(request.POST, instance=device)
        if formset.is_valid():
            formset.save()
            return redirect("device:device_detail", pk=device.id)
    else:
        formset = DeviceVerificationFormset(instance=device)

    return render(
        request,
        "device/device_update_verification_list_modal.html",
        {"device": device, "formset": formset},
    )


class DeviceWithoutVerificationListView(LoginRequiredMixin, ListView):
    model = Device
    template_name = "device/devices-without-verifications.html"
    context_object_name = "devices"

    def get_queryset(self):
        return DeviceServices.get_devices_without_verification()
