import logging

from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import path, reverse

from config import settings
from .forms import TypeToRegistryImportForm
from .models import (
    # metering_unit
    UserToOrganization,
    Address,
    MeteringUnit,
    Region,
    TypeStreet,
    Street,
    Organization,
    # device
    InstallationPoint,
    SIName,
    RegistryNumber,
    TypeName,
    TypeRegistry,
    Device,
    Verification,
    TypeToRegistryImport,
)
from apps.device.servises.file_services import check_csv_file, get_file_encoding
from apps.device.tasks.file_tasks import download_type_from_file_into_db

logger = logging.getLogger(__name__)


class OrganizationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "slug",
        "created_at",
        "updated_at",
    )

    list_display_links = ("id", "name")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


class VerificationsInLineAdmin(admin.StackedInline):
    model = Verification
    extra = 0


class DeviceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "metering_unit",
        "installation_point",
        "name",
        # "type_of_file",
        "registry_number",
        "type",
        "modification",
        "factory_number",
        "valid_date",
        "notes",
        "created_at",
        "updated_at",
    )
    inlines = [VerificationsInLineAdmin]


class VerificationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "device",
        "mit_title",
        "mit_number",
        "mit_notation",
        "mi_modification",
        "mi_number",
        "org_title",
        "verification_date",
        "valid_date",
        "is_actual",
        "is_published",
        "created_at",
        "updated_at",
    )


class TypeRegistryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "type",
        "number_registry",
        "created_at",
        "updated_at",
    )
    ordering = (
        "id",
        "type",
        "number_registry",
        "created_at",
        "updated_at",
    )

    def get_urls(self):
        urls = super().get_urls()
        urls.insert(-1, path("csv-upload/", self.upload_csv))
        return urls

    # если пользователь открыл url 'csv-upload/',
    # то он выполнит этот метод,
    # который работает с формой
    def upload_csv(self, request):
        if request.method == "POST":
            #  т.к. это метод POST проводим валидацию данных
            form = TypeToRegistryImportForm(request.POST, request.FILES)
            if form.is_valid():
                # сохраняем загруженный файл и делаем запись в базу
                form_object = form.save()
                file_path = form_object.csv_file.path
                file_encoding = get_file_encoding(file_path)
                if not check_csv_file(
                    file_path,
                    settings.FIELDNAMES_FILE_TYPE,
                    encoding=file_encoding,
                ):
                    # обновляем страницу пользователя
                    # с информацией о какой-то ошибке
                    messages.warning(request, "Неверные заголовки у файла")
                    return HttpResponseRedirect(request.path_info)

                # обработка csv файла
                logger.debug(f"{file_path=}")
                download_type_from_file_into_db.delay(file_path, file_encoding)
            # возвращаем пользователя на главную с сообщением об успехе
            url = reverse("admin:index")
            messages.success(request, "Файл будет импортирован")

            return HttpResponseRedirect(url)

        # если это не метод POST, то возвращается форма с шаблоном
        form = TypeToRegistryImportForm()
        return render(request, "admin/csv_import_page.html", {"form": form})


class SINameAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "order",
    )
    ordering = ("order",)


class InstallationPointAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "order",
    )
    ordering = ("order",)


class TypeNameAdmin(admin.ModelAdmin):
    list_display = (
        "type",
        "name",
    )
    ordering = ("name__order", "type")


admin.site.register(UserToOrganization)
admin.site.register(Address)
admin.site.register(MeteringUnit)
admin.site.register(Region)
admin.site.register(TypeStreet)
admin.site.register(Street)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(InstallationPoint, InstallationPointAdmin)
admin.site.register(SIName, SINameAdmin)
admin.site.register(RegistryNumber)
admin.site.register(TypeName, TypeNameAdmin)
admin.site.register(TypeToRegistryImport)
admin.site.register(Device, DeviceAdmin)
admin.site.register(Verification, VerificationAdmin)
admin.site.register(TypeRegistry, TypeRegistryAdmin)
