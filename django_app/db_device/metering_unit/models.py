from django.contrib.auth.models import User
from django.db import models


class BaseTimeModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Organization(BaseTimeModel):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "organizations"

    def __str__(self):
        return self.name


class UserToOrganization(BaseTimeModel):
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        related_name="user_to_org",
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        null=True,
        related_name="user_to_org",
    )
    actual = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "users_to_organizations"

    def __str__(self):
        return f"{self.user.username} ({self.organization.name})"


class Region(BaseTimeModel):
    name = models.CharField(max_length=100)
    parent_region = models.ForeignKey(
        "self", on_delete=models.PROTECT, null=True, blank=True
    )


class TypeStreet(BaseTimeModel):
    name = models.CharField(max_length=10, unique=True)
    fullname = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Street(BaseTimeModel):
    name = models.CharField(max_length=100, unique=True)
    type_street = models.ForeignKey(TypeStreet, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.type_street} {self.name}"


class Address(BaseTimeModel):
    city = models.CharField(max_length=100, blank=True)
    region = models.ForeignKey(Region, on_delete=models.PROTECT, null=True, blank=True)
    street = models.CharField(max_length=100, blank=True)
    street_new = models.ForeignKey(
        Street, on_delete=models.PROTECT, null=True, blank=True
    )
    house_number = models.CharField(max_length=100, blank=True)
    corp = models.CharField(max_length=100, blank=True)
    liter = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name_plural = "addresses"

    def __str__(self):
        return ",".join(
            map(
                str,
                (
                    self.city,
                    self.street,
                    self.house_number,
                    self.corp,
                    self.liter,
                ),
            )
        )


class MeteringUnit(BaseTimeModel):

    customer = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name="mu_c",
    )
    service_organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="mu_so",
    )
    tso = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name="mu_tso",
    )
    address = models.ForeignKey(
        Address,
        on_delete=models.PROTECT,
        related_name="mu_address",
    )
    itp = models.CharField(max_length=10, blank=True)
    totem_number = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name_plural = "metering_units"

    def __str__(self):
        return f"{self.address} {self.itp}"
