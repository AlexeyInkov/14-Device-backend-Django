import logging

from celery import shared_task
from django.db.models import Max

from apps.device.models import Device
from apps.device.servises.arshin_servises import request_to_arshin
from apps.device.servises.db_services import save_verification


logger = logging.getLogger(__name__)


@shared_task(name="tasks.refresh_all_valid_date")
def refresh_valid_date() -> str:
    logger.info("run refresh_valid_date")
    # TODO получение и сортировка device
    devices = (
        Device.objects.annotate(updated=Max("verifications__updated_at"))
        .values("id")
        .order_by("updated")
    )  # [:count_devices_in_task]
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

            response = request_to_arshin(
                reg_number.number_registry.registry_number, device.factory_number
            )
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
