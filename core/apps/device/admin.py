import csv
import logging
import os

from django.contrib import admin, messages
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import path, reverse

from config import settings
from .forms import TypeToRegistryImportForm
from .models import (
    # metering_unit
    TypeToRegistry,
    UserToOrganization,
    Address,
    MeteringUnit,
    Region,
    TypeStreet,
    Street,
    Organization,
    # device
    DeviceInstallationPoint,
    DeviceRegistryNumber,
    DeviceType,
    DeviceMod,
    Device,
    DeviceVerification,
)
from ..frontend.servises.file_services import check_csv_file

logger = logging.getLogger(__name__)

admin.site.register(UserToOrganization)
admin.site.register(Address)
admin.site.register(MeteringUnit)
admin.site.register(Region)
admin.site.register(TypeStreet)
admin.site.register(Street)


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'created_at', 'updated_at',)

    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Organization, OrganizationAdmin)

admin.site.register(DeviceInstallationPoint)
admin.site.register(DeviceRegistryNumber)
admin.site.register(DeviceType)
admin.site.register(DeviceMod)
admin.site.register(Device)


class DeviceVerificationAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'device',
                    'mi_mititle',
                    'mit_mitnumber',
                    'mi_mitype',
                    'mi_modification',
                    'mi_number',
                    'org_title',
                    'verification_date',
                    'valid_date',
                    'is_actual',
                    'is_delete',
                    'created_at',
                    'updated_at',
                    )


admin.site.register(DeviceVerification, DeviceVerificationAdmin)


class TypeToRegistryAdmin(admin.ModelAdmin):
    list_display = ('id', 'device_type_file', 'numbers_registry', 'created_at', 'updated_at',)

    def get_urls(self):
        urls = super().get_urls()
        urls.insert(-1, path('csv-upload/', self.upload_csv))
        return urls

    # если пользователь открыл url 'csv-upload/',
    # то он выполнит этот метод,
    # который работает с формой
    def upload_csv(self, request):
        if request.method == 'POST':
            #  т.к. это метод POST проводим валидацию данных
            form = TypeToRegistryImportForm(request.POST, request.FILES)
            if form.is_valid():
                # сохраняем загруженный файл и делаем запись в базу
                form_object = form.save()
                # TODO разобраться с кодировкой
                if not check_csv_file(form_object.csv_file.path, settings.FIELDNAMES_FILE_TYPE, encoding='utf-8'):
                    # обновляем страницу пользователя
                    # с информацией о какой-то ошибке
                    messages.warning(request, 'Неверные заголовки у файла')
                    return HttpResponseRedirect(request.path_info)

                # обработка csv файла
                with open(form_object.csv_file.path, mode='r', encoding='utf-8', newline='') as csv_file:
                    rows = csv.DictReader(csv_file, delimiter=';')
                    messages.success(request, 'File loading ...')
                    for row in rows:
                        print(row)
                        data = {
                            "device_type_file": row[settings.FIELDNAMES_FILE_TYPE[0]],
                            "numbers_registry": row[settings.FIELDNAMES_FILE_TYPE[1]]
                        }
                        with transaction.atomic():
                            instance, created = TypeToRegistry.objects.get_or_create(device_type_file=data['device_type_file'])

                            if not instance.numbers_registry:
                                instance.numbers_registry = data['numbers_registry']
                            else:
                                cur = set(map(int, instance.numbers_registry.split(',')))

                                new = list(map(int, data['numbers_registry'].split(',')))

                                cur = cur.union(new)

                                instance.numbers_registry = ','.join(map(str, cur))
                            if created:
                                logger.info(f'{instance} create')
                            else:
                                logger.info(f'{instance} update')
                            instance.save()
                os.remove(form_object.csv_file.path)
            # возвращаем пользователя на главную с сообщением об успехе
            url = reverse('admin:index')
            messages.success(request, 'Файл успешно импортирован')

            return HttpResponseRedirect(url)

        # если это не метод POST, то возвращается форма с шаблоном
        form = TypeToRegistryImportForm()
        return render(request, 'admin/csv_import_page.html', {'form': form})


admin.site.register(TypeToRegistry, TypeToRegistryAdmin)
