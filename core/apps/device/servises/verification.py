from typing import Dict

from django.db import transaction
from django.db.models import QuerySet

from apps.device.models import Device, Verification
from apps.device.repository import Repository
from apps.device.servises.base_service import BaseService
from apps.device.servises.database import logger
from apps.device.servises.device import DeviceServices


class VerificationServices(BaseService):
    repository = Repository("Verification")

    @classmethod
    def get_by_device(cls, device: Device) -> QuerySet:
        logger.info("Running get_verifications")
        return (
            cls.repository.get_all()
            .filter(device=device)
            .filter(is_published=True)
            .order_by("-is_actual", "-verification_date")
        )

    @classmethod
    def save_verification(cls, device_id: int, verification_fields: dict) -> None:
        logger.info("Running save_verification")
        model_fields = cls.convert_verification_field(device_id, verification_fields)
        with transaction.atomic():
            verification = cls.repository.get_or_create(**model_fields)
            logger.debug(f"{verification=}")

    @staticmethod
    def convert_verification_field(
        device_id: int, verification_fields: Dict[str, str]
    ) -> Dict[str, str]:
        logger.info("Running convert_verification_field")
        logger.debug(f"{verification_fields=}")
        model_fields = {}
        for field_name in verification_fields:
            if field_name[-4:] == "date":
                model_fields[field_name] = "-".join(
                    verification_fields[field_name][:10].split(".")[-1::-1]
                )
        model_fields["device"] = DeviceServices.get(pk=device_id)
        logger.debug(f"{model_fields=}")
        return model_fields
