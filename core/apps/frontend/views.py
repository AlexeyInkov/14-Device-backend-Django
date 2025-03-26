import os

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic import TemplateView, ListView, DetailView

import apps.frontend.servises.db_services as db_services
import apps.frontend.servises.request_services as request_services
from apps.device.models import Device
from apps.frontend.forms import UploadFileForm, DeviceVerificationFormset
from apps.frontend.mixins import ContextDataMixin, TemplateMixin
from apps.frontend.servises.file_services import handle_uploaded_file
from apps.frontend.tasks import (
    download_device_from_file_into_db,
    refresh_valid_date,
    create_excel_file,
)


class IndexView(ContextDataMixin, LoginRequiredMixin, TemplateView):
    template_name = "frontend/index.html"
    title_page = "Главная страница"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        org_selected = request_services.get_org_selected(self.request)
        if org_selected:
            context["select_org"] = db_services.get_select_org(org_selected)
        return context


class UserOrganizationsListView(TemplateMixin, LoginRequiredMixin, ListView):
    template_name = "frontend/user_organizations_list.html"
    title_page = "Организации пользователя"
    context_object_name = "user_orgs_for_select"

    def get_queryset(self):
        return db_services.get_orgs_for_select(user=self.request.user)


@login_required
def upload_device_from_file_view(request):
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
    return render(request, "frontend/modal-load-file.html", {"form": form})


@login_required
def download_device_to_file_view(request):
    metering_units = db_services.get_metering_units(
        user=request.user,
        org_selected=request_services.get_org_selected(request),
        tso_selected=request_services.get_tso_selected(request),
        cust_selected=request_services.get_cust_selected(request),
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
        "frontend/message.html",
        context={"message": "File not found", "mu": metering_units},
    )


@login_required
def refresh_valid_date_view(request):
    refresh_valid_date.delay()
    # TODO: сделать попап сообщение об успехе
    return redirect("frontend:home")


class MeteringUnitListView(
    TemplateMixin, ContextDataMixin, LoginRequiredMixin, ListView
):
    template_name = "frontend/metering_unit_list.html"
    title_page = "Узлы учета"
    context_object_name = "metering_units"

    def get_queryset(self):
        return db_services.get_metering_units(
            user=self.request.user,
            org_selected=request_services.get_org_selected(self.request),
            tso_selected=request_services.get_tso_selected(self.request),
            cust_selected=request_services.get_cust_selected(self.request),
        )


class MenuItemListView(TemplateMixin, ContextDataMixin, LoginRequiredMixin, ListView):
    template_name = "frontend/menu_item_list.html"
    title_page = "Пункты меню"
    context_object_name = "menu_items"

    def get_queryset(self):
        return (
            db_services.get_metering_units(
                user=self.request.user,
                org_selected=request_services.get_org_selected(self.request),
                tso_selected=request_services.get_tso_selected(self.request),
                cust_selected=request_services.get_cust_selected(self.request),
            )
            .values("tso__name", "tso__slug")
            .distinct()
        )


class MenuItemDetailView(TemplateMixin, ContextDataMixin, LoginRequiredMixin, ListView):
    template_name = "frontend/menu_item_detail.html"
    title_page = "Пункт меню"
    context_object_name = "menu_item"

    def get_queryset(self):
        return (
            db_services.get_metering_units(
                user=self.request.user,
                org_selected=request_services.get_org_selected(self.request),
                tso_selected=request_services.get_tso_selected(self.request),
                cust_selected=request_services.get_cust_selected(self.request),
            )
            .values("customer__name", "customer__slug")
            .distinct()
        )


class DeviceListView(TemplateMixin, ContextDataMixin, LoginRequiredMixin, ListView):
    template_name = "frontend/device_list.html"
    title_page = "Приборы"
    context_object_name = "devices"

    def get_queryset(self):
        return db_services.get_devices(
            user=self.request.user,
            org_selected=request_services.get_org_selected(self.request),
            tso_selected=request_services.get_tso_selected(self.request),
            cust_selected=request_services.get_cust_selected(self.request),
            mu_selected=request_services.get_mu_selected(self.request),
        )


class DeviceDetailView(ContextDataMixin, LoginRequiredMixin, DetailView):
    model = Device
    template_name = "frontend/device_detail_verification_list_modal.html"
    title_page = "Поверки"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        device = self.get_object()
        context["verifications"] = db_services.get_verifications(device)
        return context


@login_required
def device_verifications_update_view(request, pk):
    """Edit children and their addresses for a single parent."""

    device = get_object_or_404(Device, id=pk)

    if request.method == "POST":
        formset = DeviceVerificationFormset(request.POST, instance=device)
        if formset.is_valid():
            formset.save()
            return redirect("frontend:device_detail", pk=device.id)
    else:
        formset = DeviceVerificationFormset(instance=device)

    return render(
        request,
        "frontend/device_update_verification_list_modal.html",
        {"device": device, "formset": formset},
    )
