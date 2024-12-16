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
