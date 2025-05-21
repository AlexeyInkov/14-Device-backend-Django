import logging

from django.contrib.auth.models import User
from django.db.models import QuerySet, Q

from apps.device.repository import Repository
from apps.device.servises.base_service import BaseService
from apps.device.servises.organization import OrganizationServices

logger = logging.getLogger(__name__)


class MeteringUnitServices(BaseService):
    repository = Repository("MeteringUnit")

    @classmethod
    def get_by_user_orgs(cls, user_orgs: QuerySet) -> QuerySet:

        logger.info("Running get_by_user_orgs")
        return (
            cls.repository.get_all()
            .select_related("address__region__parent_region")
            .select_related("address__street__type_street")
            .select_related("customer")
            .select_related("tso")
            .select_related("service_organization")
            .only(
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
            .filter(
                Q(tso__in=user_orgs)
                | Q(customer__in=user_orgs)
                | Q(service_organization__in=user_orgs)
            )
        )

    @classmethod
    def get_filter_metering_units(
        cls,
        user: User,
        org_selected: str | None,
        tso_selected: str | None,
        cust_selected: str | None,
    ) -> QuerySet:

        logger.info("Running get_filter_metering_units")

        user_orgs = OrganizationServices.get_by_user(user)
        metering_units = cls.get_by_user_orgs(user_orgs)

        if org_selected is not None and org_selected != "all":
            select_org = OrganizationServices.get(slug=org_selected)
            metering_units = metering_units.filter(
                Q(tso=select_org)
                | Q(customer=select_org)
                | Q(service_organization=select_org)
            )
        filters = {}
        if tso_selected is not None and tso_selected != "all":
            filters["tso__slug"] = tso_selected
        if cust_selected is not None and cust_selected != "all":
            filters["customer__slug"] = cust_selected
        if filters:
            metering_units = metering_units.filter(**filters)
        return metering_units

    @classmethod
    def get_menu_list(
        cls,
        user: User,
        org_selected: str | None,
        tso_selected: str | None,
        cust_selected: str | None,
    ) -> QuerySet:
        return (
            cls.get_filter_metering_units(
                user, org_selected, tso_selected, cust_selected
            )
            .values("tso__name", "tso__slug")
            .distinct()
        )

    @classmethod
    def get_menu_items(
        cls,
        user: User,
        org_selected: str | None,
        tso_selected: str | None,
        cust_selected: str | None,
    ) -> QuerySet:
        return (
            cls.get_filter_metering_units(
                user, org_selected, tso_selected, cust_selected
            )
            .values("customer__name", "customer__slug")
            .distinct()
        )
