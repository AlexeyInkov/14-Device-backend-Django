from django.contrib import admin

from .models import (
    UserToOrganization,
    Organization,
    Address,
    MeteringUnit,
    Region,
    Street,
    TypeStreet,
)

admin.site.register(UserToOrganization)
admin.site.register(Organization)
admin.site.register(Address)
admin.site.register(MeteringUnit)
admin.site.register(Region)
admin.site.register(TypeStreet)
admin.site.register(Street)
