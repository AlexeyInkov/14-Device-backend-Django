from django import template

from metering_unit.models import MeteringUnit, Organization

register = template.Library()


@register.inclusion_tag('frontend/list_organizations.html')
def show_organizations(org_selected=0):
    orgs = Organization.objects.filter(pk__in=(
            MeteringUnit.objects
            .values("tso")
            .distinct()
        ))
    return {'orgs': orgs, 'org_selected': org_selected}
