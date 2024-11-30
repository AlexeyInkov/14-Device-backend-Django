from django.contrib import admin

from .models import (
    DeviceInstallationPoint,
    DeviceRegistryNumber,
    DeviceType,
    DeviceMod,
    Device,
    DeviceVerification,
    TypeToRegistry,
)


admin.site.register(DeviceInstallationPoint)
admin.site.register(DeviceRegistryNumber)
admin.site.register(DeviceType)
admin.site.register(DeviceMod)
admin.site.register(Device)
admin.site.register(DeviceVerification)
admin.site.register(TypeToRegistry)
