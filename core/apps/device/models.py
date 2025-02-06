from django.contrib.auth.models import User
from django.db import models
from slugify import slugify


class BaseTimeModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Organization(BaseTimeModel):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "organizations"

    def save(self, *args, **kwargs):
        if not self.id and not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

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

    def __str__(self):
        if self.parent_region:
            return f"{self.parent_region.name}, {self.name}"
        return f"{self.name}"


class TypeStreet(BaseTimeModel):
    name = models.CharField(max_length=10, unique=True, blank=True)
    fullname = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class Street(BaseTimeModel):
    name = models.CharField(max_length=100)
    type_street = models.ForeignKey(
        TypeStreet, on_delete=models.PROTECT, blank=True, null=True
    )

    def __str__(self):
        return f"{self.type_street} {self.name}"


class Address(BaseTimeModel):
    region = models.ForeignKey(Region, on_delete=models.PROTECT, null=True, blank=True)
    street = models.ForeignKey(Street, on_delete=models.PROTECT, null=True, blank=True)
    house_number = models.CharField(max_length=100, blank=True)
    corp = models.CharField(max_length=100, blank=True)
    liter = models.CharField(max_length=100, blank=True)
    latitude = models.FloatField(default=60)
    longitude = models.FloatField(default=30)

    class Meta:
        verbose_name_plural = "addresses"

    def __str__(self):
        address = []
        if self.region:
            address.append(str(self.region))
        if self.street:
            address.append(str(self.street))
        if self.house_number:
            address.append(f"д. {str(self.house_number)}")
        if self.corp:
            address.append(f"корп. {str(self.corp)}")
        if self.liter:
            address.append(f"лит {str(self.liter)}")
        address.append(f"({self.latitude}, {self.longitude})"),
        return ", ".join(address)


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


class RegistryNumber(BaseTimeModel):
    registry_number = models.CharField(unique=True, max_length=10)

    class Meta:
        verbose_name_plural = "registry_numbers"

    def __str__(self):
        return str(self.registry_number)


class TypeName(BaseTimeModel):
    type = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "types"

    def __str__(self):
        return self.type


class Modification(BaseTimeModel):
    mod = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "mods"

    def __str__(self):
        return self.mod


class InstallationPoint(BaseTimeModel):
    name = models.CharField(max_length=100, unique=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name_plural = "installation_points"
        ordering = ['order']

    def __str__(self):
        return self.name


class TypeToRegistry(BaseTimeModel):
    device_type_file = models.CharField(max_length=100, unique=True)
    numbers_registry = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "types_to_registry"

    def __str__(self):
        return f"{self.device_type_file} - ({self.numbers_registry})"


class TypeToRegistryImport(models.Model):
    csv_file = models.FileField(upload_to="uploads/")
    date_added = models.DateTimeField(auto_now_add=True)


class SIName(BaseTimeModel):
    name = models.CharField(max_length=100, unique=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name_plural = "si_names"
        ordering = ["order"]

    def __str__(self):
        return self.name


class Device(BaseTimeModel):
    metering_unit = models.ForeignKey(
        MeteringUnit,
        on_delete=models.PROTECT,
        null=True,
        related_name="devices",
    )
    installation_point = models.ForeignKey(
        InstallationPoint,
        on_delete=models.PROTECT,
        null=True,
        related_name="devices",
    )
    si_name = models.ForeignKey(
        SIName,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="devices"
    )
    registry_number = models.ForeignKey(
        RegistryNumber,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="devices",
    )
    type = models.ForeignKey(
        TypeName,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="devices",
    )
    mod = models.ForeignKey(
        Modification,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="devices",
    )
    type_of_file = models.ForeignKey(
        TypeToRegistry,
        on_delete=models.PROTECT,
        null=True,
        related_name="devices",
    )
    factory_number = models.CharField(max_length=100, unique=True)

    notes = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name_plural = "devices"

    @property
    def device_type(self):
        if self.registry_number:
            return f"{self.type.type}({str(self.mod.mod)})"
        else:
            return f"{self.type_of_file.device_type_file}"

    def __str__(self):
        return f"{str(self.type_of_file)} №{self.factory_number}"


class Verification(BaseTimeModel):
    device = models.ForeignKey(
        Device,
        on_delete=models.PROTECT,
        null=True,
        related_name="verifications",
    )
    mi_mititle = models.CharField(max_length=200, blank=True, null=True)
    mit_mitnumber = models.CharField(max_length=10, blank=True, null=True)
    mi_mitype = models.CharField(max_length=100, blank=True, null=True)
    mi_modification = models.CharField(max_length=100, blank=True, null=True)
    mi_number = models.CharField(max_length=20, blank=True, null=True)
    org_title = models.CharField(max_length=100, blank=True, null=True)
    verification_date = models.DateField(default="1900-01-01")
    valid_date = models.DateField(default="1900-01-01")
    is_actual = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "verifications"

    def save(self, *args, **kwargs):
        """
        device have single is_actual verification
        """
        # TODO перенести в celery tasks и atomic transactions
        if self.is_actual:
            for verification in Verification.objects.filter(device=self.device):
                verification.is_actual = False
                verification.save()
            self.is_actual = True
            # device_type, _ = DeviceType.objects.get_or_create(type=self.mi_mitype)
            if self.mi_modification:
                self.device.mod = Modification.objects.get_or_create(
                    mod=self.mi_modification
                )[0]
            if self.mi_mitype:
                self.device.type = TypeName.objects.get_or_create(type=self.mi_mitype)[
                    0
                ]
            self.device.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.valid_date}"
