from django import template

from metering_unit.models import MeteringUnit, Organization

register = template.Library()


@register.inclusion_tag('frontend/list_tso.html')
def show_tso(tso_selected):
    tso_s = Organization.objects.filter(pk__in=(
        MeteringUnit.objects
        .values("tso")
        .distinct()
    ))
    return {'tso_s': tso_s, 'tso_selected': tso_selected}


@register.inclusion_tag('frontend/list_customers.html')
def show_customers(tso_selected, cust_selected):
    if tso_selected is None:
        return {'customers': [], 'tso_selected': tso_selected, 'cust_selected': cust_selected}
    customers = Organization.objects.filter(pk__in=(
        MeteringUnit.objects.filter(tso=tso_selected)
        .values("customer")
        .distinct()
    ))
    return {'customers': customers, 'tso_selected': tso_selected, 'cust_selected': cust_selected}
