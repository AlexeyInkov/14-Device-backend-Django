import csv
import logging
import os.path

from celery import shared_task
from celery_singleton import Singleton
from django.contrib.auth import get_user_model
from django.db import transaction

from apps.device.models import (
    Organization,
    UserToOrganization,
    Region,
    TypeStreet,
    Street,
    Address,
    MeteringUnit,
    DeviceInstallationPoint,
    TypeToRegistry,
    Device,
    DeviceVerification
)
from apps.frontend.servises.arshin_servises import request_to_arshin
from apps.frontend.servises.db_services import save_verification, get_or_create_instance
from apps.frontend.servises.file_services import check_csv_file
from config import settings


logger = logging.getLogger(__name__)


@shared_task(base=Singleton, name='tasks.refresh_all_valid_date')
def refresh_valid_date() -> str:
    logger.info("run refresh_valid_date")
    devices = Device.objects.all().order_by("updated_at").only("id")
    for index, device in enumerate(devices):
        logger.info("index=", index)
        # get_device_verifications.delay(device.pk)
        logger.info("run get_device_verifications")
        for reg_number in device.type_of_file.numbers_registry.split(","):
            response = request_to_arshin(reg_number, device.factory_number)
            if response.status_code == 200:
                response = response.json()["response"]
                if response['numFound'] > 0:
                    verifications = response["docs"]
                    if verifications:
                        for verification in verifications:
                            save_verification(device.id, verification)
    return "Done"


@shared_task(name='tasks.download_device_from_file_into_db')
def download_file_to_db(filename: str, user_id: str):
    filename = os.path.join(settings.FILE_UPLOAD_DIR, filename)

    logger.info(filename)

    error_filename = "".join((filename[:-4], "_error", filename[-4:]))

    logger.info(error_filename)

    if not check_csv_file(filename, settings.FIELDNAMES_FILE_MU):

        logger.info('bad format file')

        raise ValueError

    logger.info('good format file')

    with open(filename, "r", encoding='cp1251') as file:

        logger.info('open file')

        reader = csv.DictReader(file, delimiter=";")
        with open(error_filename, "w", encoding='cp1251', newline='') as csv_file:

            logger.info('open error file')

            fieldnames = reader.fieldnames
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=";")
            writer.writeheader()
            count_error = 0

            for row in reader:
                try:
                    user = get_user_model().objects.get(id=user_id)
                    customer = {
                        "name": row["Наименование абонента"].strip(),
                    }
                    customer_id = get_or_create_instance(Organization, data=customer)

                    user_to_organization = {'user': user, 'organization': customer_id}
                    get_or_create_instance(UserToOrganization, data=user_to_organization)

                    tso = {"name": row["ТСО"].strip()}
                    tso_id = get_or_create_instance(Organization, data=tso)

                    user_to_organization = {'user': user, 'organization': tso_id}
                    get_or_create_instance(UserToOrganization, data=user_to_organization)

                    region = {"name": row["Город"].strip()}
                    region_id = get_or_create_instance(Region, data=region)

                    type_street = {"name": row['Тип улицы'].strip()}
                    if not type_street:
                        type_street = " "
                        print("-------------------------------Васька---------------------------")
                    type_street_id = get_or_create_instance(TypeStreet, data=type_street)

                    street = {"name": row["Наименование улицы"].strip()}
                    if type_street_id:
                        street.update({"type_street": type_street_id})
                    street_id = get_or_create_instance(Street, data=street)

                    address = {
                        "region": region_id,
                        "street": street_id,
                        "house_number": row["№ дома"].strip(),
                        "corp": row["Корп"].strip(),
                        "liter": row["Лит"].strip(),

                    }
                    address_id = get_or_create_instance(Address, data=address)

                    metering_unit = {
                        'customer': customer_id,
                        'tso': tso_id,
                        'address': address_id,
                        'itp': row["ТЦ"].strip(),
                        'totem_number': row["№ Тотэм"].strip(),
                    }
                    metering_unit_id = get_or_create_instance(MeteringUnit, data=metering_unit)

                    installation_point = {'name': row["Труба"].strip()}
                    installation_point_id = get_or_create_instance(DeviceInstallationPoint, data=installation_point)

                    type_of_file = {'device_type_file': row["Тип"].strip()}
                    type_of_file_id = get_or_create_instance(TypeToRegistry, data=type_of_file)

                    # mod = row["Ду"]
                    # mod_id = req_api('device/mod/', body=mod, headers=headers)['id']

                    device = {
                        'metering_unit': metering_unit_id,
                        'installation_point': installation_point_id,
                        'type_of_file': type_of_file_id,
                        'factory_number': row["Номер"].strip(),
                    }
                    device_id = get_or_create_instance(Device, data=device)

                    data = row["Дата"].strip()
                    if data:
                        data = data.split('.')

                        device_verification = {
                            'device': device_id,
                            'valid_date': '-'.join((data[2], data[1], data[0])),
                        }
                        print(device_verification)
                        get_or_create_instance(DeviceVerification, data=device_verification)
                except BaseException as e:
                    logger.info(e)
                    writer.writerow(row)
                    count_error += 1

                logger.info(count_error)
                if count_error > 0:
                    raise Exception(f"{count_error} error")
    if count_error == 0:
        os.remove(filename)
        os.remove(error_filename)


# TODO новые tasks
def user_to_org_create(id):
    pass


def device_field():
    pass
