from django.db import transaction
from django.db.models import Q

from device.models import Device
from metering_unit.models import Organization, MeteringUnit


def get_devices(mu_selected, metering_units):
    devices = (
        Device.objects.only(
            "installation_point__name",
            "registry_number__registry_number",
            "type__type",
            "mod__mod",
            "type_of_file__device_type_file",
            "type_of_file__numbers_registry",
            "factory_number",
            "notes",
        )
        .select_related("type_of_file")
        .select_related("installation_point")
        .prefetch_related("verifications")
    )
    # Device filter
    if mu_selected and mu_selected != "all":
        return devices.filter(metering_unit=mu_selected)
    return devices.filter(metering_unit__in=metering_units.values_list("pk", flat=True))


def get_metering_units(tso_selected, cust_selected, orgs):
    metering_units = (
        MeteringUnit.objects.only(
            "customer__name",
            "address__region__name",
            "address__region__parent_region__name",
            "address__street__type_street__name",
            "address__street__name",
            "address__house_number",
            "address__corp",
            "address__liter",
            "address__latitude",
            "address__longitude",
            "itp",
            "tso__name",
            "service_organization__name",
        )
        .select_related("address__region")
        .select_related("address__street__type_street")
        .select_related("customer")
        .select_related("tso")
    ).filter(Q(tso__in=orgs) | Q(customer__in=orgs) | Q(service_organization__in=orgs))
    # MeteringUnit filter
    filters = {}
    if tso_selected != "all":
        filters["tso"] = tso_selected
    if cust_selected != "all":
        filters["customer"] = cust_selected
    if filters:
        return metering_units.filter(**filters), metering_units
    return metering_units, metering_units


def get_organizations(org_selected, user):
    orgs = Organization.objects.only("name").filter(user_to_org__user=user)
    print(orgs)
    # Orgs filter
    if org_selected != "all":
        return orgs.filter(pk=org_selected)
    return orgs


def get_customers(tso_selected, metering_units, orgs):
    filters = {}
    if tso_selected != "all":
        filters["tso"] = tso_selected
    return orgs.filter(
        id__in=(metering_units.filter(**filters).values("customer").distinct())
    )


def save_verification(device_id, verification):
    with transaction.atomic():
        print(Device.objects.get(pk=device_id))
