import logging

from django.contrib.auth.models import User
from django.db.models import QuerySet, Q, Model


from apps.device.repository import Repository
from apps.device.services.base_service import BaseService

logger = logging.getLogger(__name__)


class OrganizationServices(BaseService):
    repository = Repository("Organization")

    @classmethod
    def get_by_slug(cls, slug: str) -> Model:
        logger.info("Running get_by_slug")
        return cls.repository.get(slug=slug)

    @classmethod
    def get_by_user(cls, user: User) -> QuerySet:
        logger.info("Running get_by_user")
        return (
            cls.repository.get_all()
            .prefetch_related("user_to_org__user")
            .filter(user_to_org__user=user, user_to_org__actual=True)
        )

    @classmethod
    def get_by_metering_units(cls, metering_units: QuerySet) -> QuerySet:
        logger.info("Running get_by_metering_units")
        return (
            cls.repository.get_all()
            .prefetch_related("mu_c", "mu_so", "mu_tso")
            .filter(
                Q(mu_c__in=metering_units)
                | Q(mu_so__in=metering_units)
                | Q(mu_tso__in=metering_units)
            )
            .distinct()
        )
