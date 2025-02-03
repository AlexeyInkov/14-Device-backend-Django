import csv
import logging
import os.path

from celery import shared_task
from django.contrib.auth import get_user_model
from django.db.models import Max

from apps.device.models import (
    Device,
    Verification
)
from apps.frontend.servises.arshin_servises import request_to_arshin
from apps.frontend.servises.db_services import save_verification, write_row_to_db
from apps.frontend.servises.file_services import check_csv_file
from config import settings

logger = logging.getLogger(__name__)


@shared_task(name='tasks.refresh_all_valid_date')
def refresh_valid_date() -> str:
    logger.info("run refresh_valid_date")

    devices = Verification.objects.values('device').annotate(updated=Max('updated_at')).order_by('updated')[:50]
    logger.debug(f"{devices=}")
    # devices = Device.objects.all().order_by("updated_at").only("id")[:10]

    for index, item in enumerate(devices):
        logger.info(f"index={index}, device_id={item['device']}")
        device = Device.objects.get(pk=item['device'])
        logger.info(f"device={device}")
        # get_device_verifications.delay(device.pk)
        # logger.info("run get_device_verifications")
        for reg_number in device.type_of_file.numbers_registry.split(","):
            logger.info("request_to_arshin")
            response = request_to_arshin(reg_number, device.factory_number)
            if response.status_code == 200:
                logger.info(f"response={response.status_code}")
                response = response.json()["response"]
                logger.info(f"Found verifications in response: {response['numFound']}")
                if response['numFound'] > 0:
                    verifications = response["docs"]
                    if verifications:
                        for verification in verifications:
                            save_verification(device.id, verification)
                            logger.info("verification saved")
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
def user_to_org_create(id):
    pass


def device_field():
    pass
