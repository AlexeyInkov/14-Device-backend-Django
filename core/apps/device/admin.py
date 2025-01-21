import csv

from django.contrib import admin, messages
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import path, reverse

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

admin.site.register(UserToOrganization)
admin.site.register(Address)
admin.site.register(MeteringUnit)
admin.site.register(Region)
admin.site.register(TypeStreet)
admin.site.register(Street)


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Organization, OrganizationAdmin)

admin.site.register(DeviceInstallationPoint)
admin.site.register(DeviceRegistryNumber)
admin.site.register(DeviceType)
admin.site.register(DeviceMod)
admin.site.register(Device)
admin.site.register(DeviceVerification)


class TypeToRegistryAdmin(admin.ModelAdmin):
    list_display = ('id', 'device_type_file', 'numbers_registry')

    def get_urls(self):
        urls = super().get_urls()
        urls.insert(-1, path('csv-upload/', self.upload_csv))
        return urls

    # если пользователь открыл url 'csv-upload/',
    # то он выполнит этот метод,
    # который работает с формой
    def upload_csv(self, request):
        if request.method == 'POST':
            # т.к. это метод POST проводим валидацию данных
            form = TypeToRegistryImportForm(request.POST, request.FILES)
            if form.is_valid():
                # сохраняем загруженный файл и делаем запись в базу
                form_object = form.save()

                # обработка csv файла
                with open(form_object.csv_file.path, mode='r', encoding='utf-8', newline='') as csv_file:
                    rows = csv.reader(csv_file, delimiter=';')
                    if next(rows) != ['Тип', 'Номер в госреестре']:
                        # обновляем страницу пользователя
                        # с информацией о какой-то ошибке
                        messages.warning(request, 'Неверные заголовки у файла')
                        return HttpResponseRedirect(request.path_info)
                    for row in rows:
                        print(row)
                        data = {
                            "device_type_file": row[0],
                            "numbers_registry": row[1]
                        }
                        with transaction.atomic():
                            instance, created = TypeToRegistry.objects.get_or_create(device_type_file=data['device_type_file'])

                            if not instance.numbers_registry:
                                instance.numbers_registry = data['numbers_registry']
                            else:
                                cur = set(map(int, instance.numbers_registry.split(',')))

                                new = list(map(int,data['numbers_registry'].split(',')))

                                cur = cur.union(new)

                                instance.numbers_registry = ','.join(map(str, cur))
                            if created:
                                messages.info(request, f'{instance} create')
                            else:
                                messages.info(request, f'{instance} update')
                            instance.save()

            # возвращаем пользователя на главную с сообщением об успехе
            url = reverse('admin:index')
            messages.success(request, 'Файл успешно импортирован')
            return HttpResponseRedirect(url)

        # если это не метод POST, то возвращается форма с шаблоном
        form = TypeToRegistryImportForm()
        return render(request, 'admin/csv_import_page.html', {'form': form})


admin.site.register(TypeToRegistry, TypeToRegistryAdmin)
