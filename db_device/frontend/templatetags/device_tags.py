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
    filters = {}
    if tso_selected != 0:
        filters['tso'] = tso_selected
    customers = Organization.objects.filter(pk__in=(
        MeteringUnit.objects.filter(**filters)
        .values("customer")
        .distinct()
    ))
    return {'customers': customers, 'tso_selected': tso_selected, 'cust_selected': cust_selected}


@register.inclusion_tag('frontend/list_metering_units.html')
def show_metering_units(tso_selected, cust_selected, mu_selected):
    filters = {}
    if tso_selected != 0:
        filters['tso'] = tso_selected
    if cust_selected == '':
        cust_selected = 0
    if cust_selected != 0:
        filters['customer'] = cust_selected

    metering_units = (MeteringUnit.objects.filter(**filters)
                      .select_related('address__region')
                      .select_related('address__street__type_street')
                      )

    return {'metering_units': metering_units, 'tso_selected': tso_selected, 'cust_selected': cust_selected, 'mu_selected': mu_selected}
