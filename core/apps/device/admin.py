from django.contrib import admin

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


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(UserToOrganization)
admin.site.register(Address)
admin.site.register(MeteringUnit)
admin.site.register(Region)
admin.site.register(TypeStreet)
admin.site.register(Street)
admin.site.register(Organization, OrganizationAdmin)


admin.site.register(DeviceInstallationPoint)
admin.site.register(DeviceRegistryNumber)
admin.site.register(DeviceType)
admin.site.register(DeviceMod)
admin.site.register(Device)
admin.site.register(DeviceVerification)
admin.site.register(TypeToRegistry)
