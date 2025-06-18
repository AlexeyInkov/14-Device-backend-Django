import logging

from django.contrib.auth.models import User
from django.db.models import QuerySet

from apps.device.repository import Repository
from apps.device.services.base_service import BaseService
from apps.device.services.organization import OrganizationServices
from apps.device.services.metering_unit import MeteringUnitServices

logger = logging.getLogger(__name__)


class DeviceServices(BaseService):
    repository = Repository("Device")

    @classmethod
    def get_by_metering_unit(cls, metering_units: QuerySet) -> QuerySet:
        logger.info("Running get_by_metering_unit")
        return (
            cls.repository.get_all()
            .select_related("mit_number")
            .select_related("mit_notation")
            .select_related("mi_modification")
            .select_related("installation_point")
            .select_related("metering_unit")
            # .only(
            #     "installation_point__name",
            #     "installation_point__order",
            #     "name__order",
            #     "registry_number__registry_number",
            #     "type__type",
            #     "modification__modification",
            #     "factory_number",
            #     "notes",
            #     "metering_unit_id",
            #     "valid_date"
            # )
            .order_by(
                "metering_unit_id",
                "installation_point__order",
                "mit_notation__name__order",
            )
            .filter(metering_unit__in=metering_units)
        )

    @classmethod
    def get_devices(
        cls,
        user: User,
        org_selected: str | None,
        tso_selected: str | None,
        cust_selected: str | None,
        mu_selected: int | None,
    ) -> QuerySet:
        logger.info("Running get_devices")

        user_orgs = OrganizationServices.get_by_user(user=user)
        metering_units = MeteringUnitServices.get_by_user_orgs(user_orgs=user_orgs)
        devices = cls.get_by_metering_unit(metering_units=metering_units)
        if mu_selected is not None:
            return devices.filter(metering_unit=mu_selected)
        elif org_selected is not None:
            return devices.filter(
                metering_unit__in=MeteringUnitServices.get_filter_metering_units(
                    user=user,
                    org_selected=org_selected,
                    tso_selected=tso_selected,
                    cust_selected=cust_selected,
                )
            )
        return devices

    @classmethod
    def get_devices_without_verification(cls) -> QuerySet:
        return cls.repository.get_all().filter(verifications__isnull=True)
