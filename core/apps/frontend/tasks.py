import csv
import logging
import os
import shutil
import uuid

from celery import shared_task
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Max

import apps.frontend.servises.db_services as db_services
import apps.frontend.servises.file_services as file_services
from apps.device.models import Device, TypeRegistry, SIName, TypeName, RegistryNumber
from apps.frontend.servises.arshin_servises import request_to_arshin
from apps.frontend.servises.db_services import save_verification, write_row_to_db
from apps.frontend.servises.file_services import check_csv_file, get_file_encoding
from config import settings

logger = logging.getLogger(__name__)


@shared_task(name="tasks.refresh_all_valid_date")
def refresh_valid_date() -> str:
    logger.info("run refresh_valid_date")
    # TODO получение и сортировка device
    devices = Device.objects.annotate(updated=Max("verifications__updated_at")).values('id').order_by("updated")  # [:count_devices_in_task]
    logger.debug(f"{devices=}")

    for device_id in devices:
        logger.info(f"{device_id=}")
        try:
            device = Device.objects.get(id=device_id)
            logger.info(f"{device=}")
        except Device.DoesNotExist:
            logger.error(f"Device with id={device_id} not found")
            continue
        logger.info("get device numbers_registry")
        numbers_registry = device.type.numbers_registry.all()
        logger.debug(f"{numbers_registry=}")
        for reg_number in numbers_registry:
            logger.info(reg_number.number_registry.registry_number)
            logger.info("request_to_arshin")

            # TODO добавить начало поиска в arshin

            response = request_to_arshin(reg_number.number_registry.registry_number, device.factory_number)
            if response.status_code == 200:
                logger.info(f"response={response.status_code}")
                logger.debug(f"response={response}")
                response = response.json()["result"]
                logger.debug(f"response['result']={response}")
                logger.info(f"Found verifications in response: {response['count']}")
                if response["count"] > 0:
                    verifications = response["items"]
                    if verifications:
                        for verification in verifications:
                            logger.debug(verification)
                            save_verification(device.id, verification)
                            logger.info("verification saved")
    return "Done"


@shared_task(name="tasks.download_device_from_file_into_db")
def download_device_from_file_into_db(filename: str, user_id: str):
    filename = os.path.join(settings.FILE_UPLOAD_DIR, filename)

    logger.info(filename)

    file_encoding = get_file_encoding(filename)

    error_filename = "".join((filename[:-4], "_error", filename[-4:]))

    logger.info(error_filename)

    if not check_csv_file(filename, settings.FIELDNAMES_FILE_MU, encoding=file_encoding):
        logger.info("bad format file")
        raise ValueError

    logger.info("good format file")

    with open(filename, "r", encoding=file_encoding) as file:

        logger.info("open file")

        reader = csv.DictReader(file, delimiter=";")
        with open(error_filename, "w", encoding=file_encoding, newline="") as csv_file:

            logger.info("open error file")

            fieldnames = reader.fieldnames
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=";")
            writer.writeheader()
            count_error = 0
            user = get_user_model().objects.get(id=user_id)
            for row in reader:
                try:
                    write_row_to_db(row, user)
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
        return "Done"


# TODO новые tasks
def user_to_org_create():
    pass


def device_field():
    pass


@shared_task(name="tasks.download_type_from_file_into_db")
def download_type_from_file_into_db(file_path: str, file_encoding: str) -> None:
    with open(file_path, mode="r", encoding=file_encoding, newline="") as csv_file:
        rows = csv.DictReader(csv_file, delimiter=";")

        for row in rows:
            logger.debug(row)

            device_type = row[settings.FIELDNAMES_FILE_TYPE[0]].strip()
            numbers_registry = row[settings.FIELDNAMES_FILE_TYPE[1]].strip()
            name = row[settings.FIELDNAMES_FILE_TYPE[2]].strip()

            with transaction.atomic():
                device_name, _ = SIName.objects.get_or_create(name=name)
                device_type, _ = TypeName.objects.get_or_create(type=device_type, name=device_name)
                numbers_registry = (RegistryNumber.objects.get_or_create(registry_number=number_registry)[0] for number_registry in numbers_registry.split(","))
                for number_registry in numbers_registry:
                    type_registry, _ = TypeRegistry.objects.get_or_create(
                        type=device_type,
                        number_registry=number_registry,
                    )
    os.remove(file_path)


def create_excel_file(metering_units):
    # template = os.path.sep.join((settings.FILE_TEMPLATES_DIR, "template.xlsx"))
    file_name = os.path.sep.join((settings.FILE_UPLOAD_DIR, f'{str(uuid.uuid4()).split("-")[-1]}.xlsx'))
    # # копируем шаблон
    # shutil.copyfile(template, file_name)
    dict_list = db_services.create_dict_from_db(metering_units)
    file_services.create_excel_from_dict_list(dict_list, file_name, sheet_name='Sheet1')
    return file_name
