import datetime
import logging
from typing import Tuple, Dict

from django.db import transaction
from django.db.models import Q, QuerySet

from apps.device.models import (
    Device,
    Verification,
    Organization,
    UserToOrganization,
    Region,
    TypeStreet,
    Street,
    Address,
    MeteringUnit,
    InstallationPoint,
    TypeRegistry, TypeName,
)
from config.settings import CONVERT_VERIF_FIELDS

logger = logging.getLogger(__name__)


def get_devices(mu_selected: str, metering_units: QuerySet) -> QuerySet:
    devices = (
        Device.objects.only(
            "installation_point__name",
            "installation_point__order",
            "name__order",
            "registry_number__registry_number",
            "type__type",
            "modification__modification",
            "factory_number",
            "notes",
            "metering_unit_id",
            "valid_date"
        )
        .select_related("registry_number")
        .select_related("type")
        .select_related("modification")
        .select_related("installation_point")
        .select_related("name")
        .select_related("metering_unit")
        .order_by("metering_unit_id", "installation_point__order", "name__order")
    )
    # Device filter
    if mu_selected and mu_selected != "all":
        return devices.filter(metering_unit=mu_selected)
    return devices.filter(metering_unit__in=metering_units.values_list("pk", flat=True))


def get_metering_units(
        tso_selected: str, cust_selected: str, orgs: QuerySet
) -> Tuple[QuerySet, QuerySet]:
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
        .select_related("address__region__parent_region")
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


def get_filter_organization(
        org_selected: str, orgs: QuerySet
) -> Tuple[QuerySet, Organization | None]:
    if org_selected != "all":
        result = orgs.filter(slug=org_selected)
        return result, result.first()
    return orgs, None


def get_customers(
        tso_selected: str, metering_units: QuerySet, orgs: QuerySet
) -> QuerySet:
    filters = {}
    if tso_selected != "all":
        filters["tso__slug"] = tso_selected
    return orgs.filter(
        id__in=(metering_units.filter(**filters).values("customer").distinct())
    )


def save_verification(device_id: int, verification_fields: dict) -> None:
    logger.info("run_save_verification")
    model_fields = convert_verification_field(device_id, verification_fields)
    with transaction.atomic():
        # print(DeviceVerification.objects.filter(device=device_id))
        verification = Verification.objects.get_or_create(**model_fields)
        logger.debug(f"{verification=}")


def convert_verification_field(
        device_id: int, verification_fields: Dict[str, str]
) -> Dict[str, str]:
    logger.debug(f"{verification_fields=}")
    model_fields = {}
    for field_name in CONVERT_VERIF_FIELDS.keys():
        if verification_fields.get(CONVERT_VERIF_FIELDS[field_name], None) is not None:
            if field_name[-4:] == "date":
                model_fields[field_name] = verification_fields[
                                               CONVERT_VERIF_FIELDS[field_name]
                                           ][:10]
            else:
                model_fields[field_name] = verification_fields[
                    CONVERT_VERIF_FIELDS[field_name]
                ]
    model_fields["device"] = Device.objects.get(pk=device_id)
    logger.debug(f"{model_fields=}")
    return model_fields


def write_row_to_db(row, user):
    with transaction.atomic():
        customer = {
            "name": row["Наименование абонента"].strip(),
        }
        logger.debug(customer)
        customer_id, _ = Organization.objects.get_or_create(**customer)

        user_to_organization = {"user": user, "organization": customer_id}
        logger.debug(user_to_organization)
        UserToOrganization.objects.get_or_create(**user_to_organization)

        tso = {"name": row["ТСО"].strip()}
        logger.debug(tso)
        tso_id, _ = Organization.objects.get_or_create(**tso)

        user_to_organization = {"user": user, "organization": tso_id}
        logger.debug(user_to_organization)
        UserToOrganization.objects.get_or_create(**user_to_organization)

        region = {"name": row["Город"].strip()}
        logger.debug(region)
        region_id, _ = Region.objects.get_or_create(**region)

        type_street = {"name": row["Тип улицы"].strip()}
        if not type_street:
            type_street = " "
            print("-------------------------------Васька---------------------------")
        logger.debug(type_street)
        type_street_id, _ = TypeStreet.objects.get_or_create(**type_street)

        street = {"name": row["Наименование улицы"].strip()}
        if type_street_id:
            street.update({"type_street": type_street_id})
        logger.debug(street)
        street_id, _ = Street.objects.get_or_create(**street)

        address = {
            "region": region_id,
            "street": street_id,
            "house_number": row["№ дома"].strip(),
            "corp": row["Корп"].strip(),
            "liter": row["Лит"].strip(),
        }
        logger.debug(address)
        address_id, _ = Address.objects.get_or_create(**address)

        metering_unit = {
            "address": address_id,
            "itp": row["ТЦ"].strip(),
        }
        default = {
            "customer": customer_id,
            "tso": tso_id,
            "totem_number": row["№ Тотэм"].strip(),
        }
        logger.debug(metering_unit)
        metering_unit_id, create = MeteringUnit.objects.get_or_create(**metering_unit, defaults=default)
        if not create:
            metering_unit_id.customer = customer_id
            metering_unit_id.tso = tso_id
            metering_unit_id.totem_number = row["№ Тотэм"].strip()
            metering_unit_id.save()

        installation_point = {"name": row["Труба"].strip()}
        logger.debug(installation_point)
        installation_point_id, _ = InstallationPoint.objects.get_or_create(
            **installation_point
        )

        device_type = row["Тип"].strip()
        logger.debug(device_type)
        type_id, _ = TypeName.objects.get_or_create(type=device_type)

        # mod = row["Ду"].strip()
        # mod_id = req_api('device/mod/', body=mod, headers=headers)['id']

        data = row["Дата"].strip()
        if data:
            data = data.split(".")
            valid_date = "-".join((data[2], data[1], data[0]))
        device = {
            "metering_unit": metering_unit_id,
            "installation_point": installation_point_id,
            "type": type_id,
            "valid_date": valid_date,
            "name": type_id.name
        }
        factory_number = row["Номер"].strip()
        # TODO обработать номер для СПТ, КТПТР, СДВ-И

        logger.debug(device)
        device_id, create = Device.objects.get_or_create(factory_number=factory_number, defaults=device)

        if not create:
            device_id.metering_unit = metering_unit_id
            device_id.installation_point = installation_point_id
            device_id.type_of_file = type_id
            device_id.name = type_id.name
            if datetime.datetime.strptime(valid_date, "%Y-%m-%d").date() > device_id.valid_date:
                device_id.valid_date = valid_date
            device_id.save()
