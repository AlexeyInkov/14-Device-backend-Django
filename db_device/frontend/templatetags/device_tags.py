from django import template


register = template.Library()


@register.inclusion_tag("frontend/list_menu.html")
def show_menu(orgs, metering_units, tso_selected, cust_selected):
    tso_s = orgs.filter(pk__in=(metering_units.values("tso").distinct()))
    filters = {}
    if tso_selected != "all":
        filters["tso"] = tso_selected
    customers = orgs.filter(
        id__in=(metering_units.filter(**filters).values("customer").distinct())
    )
    return {
        "tso_s": tso_s,
        "customers": customers,
        "tso_selected": tso_selected,
        "cust_selected": cust_selected,
    }


@register.inclusion_tag("frontend/list_metering_units.html")
def show_metering_units(metering_units, tso_selected, cust_selected, mu_selected):
    filters = {}
    if tso_selected != "all":
        filters["tso"] = tso_selected
    if cust_selected != "all":
        filters["customer"] = cust_selected

    metering_units = (
        metering_units.filter(**filters)
        .select_related("address__region")
        .select_related("address__street__type_street")
    )

    return {
        "metering_units": metering_units,
        "tso_selected": tso_selected,
        "cust_selected": cust_selected,
        "mu_selected": mu_selected,
    }


@register.inclusion_tag("frontend/list_devices.html")
def show_devices(devices, tso_selected, cust_selected, mu_selected, dev_selected):
    filters = {}
    if mu_selected != "all":
        filters["metering_unit"] = mu_selected

    devices = devices.filter(**filters)

    return {
        "devices": devices,
        "tso_selected": tso_selected,
        "cust_selected": cust_selected,
        "mu_selected": mu_selected,
        "dev_selected": dev_selected,
    }


@register.inclusion_tag("frontend/list_verifications.html")
def show_devices(
    verifications,
    tso_selected,
    cust_selected,
    mu_selected,
    dev_selected,
    verif_selected,
):
    filters = {}
    if dev_selected != "all":
        filters["device"] = dev_selected

    verifications = verifications.filter(**filters)

    return {
        "verifications": verifications,
        "tso_selected": tso_selected,
        "cust_selected": cust_selected,
        "mu_selected": mu_selected,
        "dev_selected": dev_selected,
        "verif_selected": verif_selected,
    }
