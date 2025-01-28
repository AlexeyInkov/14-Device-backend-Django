from django import template


register = template.Library()
#
#
# @register.inclusion_tag("frontend/list_menu.html")
# def show_menu(orgs, metering_units, tso_selected, cust_selected):
#     tso_s = orgs.filter(pk__in=(metering_units.values("tso").distinct()))
#     filters = {}
#     if tso_selected != "all":
#         filters["tso"] = tso_selected
#     customers = orgs.filter(
#         id__in=(metering_units.filter(**filters).values("customer").distinct())
#     )
#     return {
#         "tso_s": tso_s,
#         "customers": customers,
#         "tso_selected": tso_selected,
#         "cust_selected": cust_selected,
#     }
#
#
# @register.inclusion_tag("frontend/list_metering_units.html")
# def show_metering_units(metering_units, tso_selected, cust_selected, mu_selected):
#     filters = {}
#     if tso_selected != "all":
#         filters["tso"] = tso_selected
#     if cust_selected != "all":
#         filters["customer"] = cust_selected
#
#     metering_units = (
#         metering_units.filter(**filters)
#         .select_related("address__region")
#         .select_related("address__street__type_street")
#     )
#
#     return {
#         "metering_units": metering_units,
#         "tso_selected": tso_selected,
#         "cust_selected": cust_selected,
#         "mu_selected": mu_selected,
#     }
#
#
# @register.inclusion_tag("frontend/list_devices.html")
# def show_devices(
#     metering_units, devices, tso_selected, cust_selected, mu_selected, dev_selected
# ):
#     filters = {}
#     if tso_selected != "all":
#         filters["tso"] = tso_selected
#     if cust_selected != "all":
#         filters["customer"] = cust_selected
#
#     metering_units = metering_units.filter(**filters)
#     if mu_selected and mu_selected != "all":
#         devices = devices.filter(metering_unit__in=[mu_selected])
#     else:
#         devices = devices.filter(metering_unit__in=metering_units)
#
#     return {
#         "devices": devices,
#         "tso_selected": tso_selected,
#         "cust_selected": cust_selected,
#         "mu_selected": mu_selected,
#         "dev_selected": dev_selected,
#     }


@register.inclusion_tag("frontend/includes/modal_list_verifications.html")
def show_modal_verifications(device):
    verifications = device.verifications.all()
    return {
        "device": device,
        "verifications": verifications,
    }
