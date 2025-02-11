import csv
import logging
import os

from celery import shared_task
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Max

from apps.device.models import Device, Verification, TypeRegistry, SIName, TypeName, RegistryNumber
from apps.frontend.servises.arshin_servises import request_to_arshin
from apps.frontend.servises.db_services import save_verification, write_row_to_db
from apps.frontend.servises.file_services import check_csv_file, get_file_encoding
from config import settings

logger = logging.getLogger(__name__)


@shared_task(name="tasks.refresh_all_valid_date")
def refresh_valid_date() -> str:
    logger.info("run refresh_valid_date")

    devices = (
        Verification.objects.values("device")
        .annotate(updated=Max("updated_at"))
        .order_by("updated")[:50]
    )
    if not devices:
        devices = Device.objects.all().order_by("updated_at").prefetch_related("type__numbers_registry__number_registry")[:100]
    logger.debug(f"{devices=}")

    for device in devices:
        logger.info(f"{device=}")
        # device = Device.objects.get(pk=device.id)
        # logger.info(f"device={device}")
        # get_device_verifications.delay(device.pk)
        # logger.info("run get_device_verifications")
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
                response = response.json()["response"]
                logger.info(f"Found verifications in response: {response['numFound']}")
                if response["numFound"] > 0:
                    verifications = response["docs"]
                    if verifications:
                        for verification in verifications:
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
