from typing import Tuple, Dict

from django.db import transaction, models
from django.db.models import Q, QuerySet

from apps.device.models import Device, DeviceVerification
from apps.device.models import Organization, MeteringUnit


def get_devices(mu_selected: str, metering_units: QuerySet) -> QuerySet:
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


def get_metering_units(tso_selected: str, cust_selected: str, orgs: QuerySet) -> Tuple[QuerySet, QuerySet]:
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
        filters["tso__slug"] = tso_selected
    if cust_selected != "all":
        filters["customer__slug"] = cust_selected
    if filters:
        return metering_units.filter(**filters), metering_units
    return metering_units, metering_units


def get_filter_organization(org_selected: str, orgs: QuerySet) -> Tuple[QuerySet, Organization | None]:
    if org_selected != "all":
        result = orgs.filter(slug=org_selected)
        return result, result.first()
    return orgs, None


def get_customers(tso_selected: str, metering_units: QuerySet, orgs: QuerySet) -> QuerySet:
    filters = {}
    if tso_selected != "all":
        filters["tso__slug"] = tso_selected
    return orgs.filter(
        id__in=(metering_units.filter(**filters).values("customer").distinct())
    )


def save_verification(device_id: int, verification: dict) -> None:
    print('run_save_verification')
    model_fields = get_model_field(device_id, verification)
    with transaction.atomic():
        # print(DeviceVerification.objects.filter(device=device_id))
        verification = DeviceVerification.objects.filter(device=device_id).filter(**model_fields)
        # print(verification)
        if not verification:
            new = DeviceVerification.objects.create(**model_fields)
            print("new=", new)


def get_model_field(device_id: int, verification: Dict[str, str]) -> Dict[str, str]:
    convert = {
        "mi_mititle": "mi.mititle",
        "mit_mitnumber": "mi.mitnumber",
        "mi_mitype": "mi.mitype",
        "mi_modification": "mi.modification",
        "mi_number": "mi.number",
        "org_title": "org_title",
        "verification_date": "verification_date",
        "valid_date": "valid_date"
    }
    model_fields = {}
    for field_name in convert.keys():
        if verification.get(convert[field_name]):
            if field_name[-4:] == "date":
                model_fields[field_name] = verification[convert[field_name]][:10]
            else:
                model_fields[field_name] = verification[convert[field_name]]
    model_fields["device"] = Device.objects.get(pk=device_id)
    return model_fields


def get_or_create_instance(model: models, data: dict) -> models.Model:
    instance = model.objects.get_or_create().filter(**data)
    if len(instance) > 1:
        # log
        raise Exception("Duplicate instance")
    instance = instance.first()
    if not instance:
        instance = model.objects.create(**data)
        # log
    return instance
