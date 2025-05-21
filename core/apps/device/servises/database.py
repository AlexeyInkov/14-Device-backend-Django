import datetime
import logging

from django.db import transaction
from django.db.models import QuerySet

from apps.device.models import (
    Device,
    Organization,
    UserToOrganization,
    Region,
    TypeStreet,
    Street,
    Address,
    MeteringUnit,
    InstallationPoint,
    TypeName,
)
from apps.device.servises.device import DeviceServices

logger = logging.getLogger(__name__)


def write_row_to_db(row, user):
    logger.info("Running write_row_to_db")

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
        metering_unit_id, create = MeteringUnit.objects.get_or_create(
            **metering_unit, defaults=default
        )
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
            "name": type_id.name,
        }
        factory_number = row["Номер"].strip()
        # TODO обработать номер для СПТ, КТПТР, СДВ-И

        logger.debug(device)
        device_id, create = Device.objects.get_or_create(
            factory_number=factory_number, defaults=device
        )

        if not create:
            device_id.metering_unit = metering_unit_id
            device_id.installation_point = installation_point_id
            device_id.type_of_file = type_id
            device_id.name = type_id.name
            if (
                datetime.datetime.strptime(valid_date, "%Y-%m-%d").date()
                > device_id.valid_date
            ):
                device_id.valid_date = valid_date
            device_id.save()


def create_dict_from_db(metering_units: QuerySet) -> list[dict]:
    logger.info("Running create_dict_from_db")
    lst = []
    for metering_unit in metering_units:
        for device in DeviceServices.get_all().filter(metering_unit=metering_unit):
            dct = {
                "№ п/п": metering_unit.id,
                "Наименование абонента": metering_unit.customer.name,
                "Город": metering_unit.address.region.name,
                "Наименование улицы": metering_unit.address.street.name,
                "Тип улицы": metering_unit.address.street.type_street.name,
                "№ дома": metering_unit.address.house_number,
                "Корп": metering_unit.address.corp,
                "Лит": metering_unit.address.liter,
                "ТЦ": metering_unit.itp,
                "Труба": device.installation_point.name,
                "Тип": device.type.type,
                "Ду": "",
                "Номер": device.factory_number,
                "Дата": device.valid_date,
                "МПИ": "",
                "ТСО": metering_unit.tso.name,
                "№ Тотэм": "",
            }
            lst.append(dct)
    return lst
