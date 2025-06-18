import logging

from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.device.models import (
    Verification,
    RegistryNumber,
    TypeName,
    Modification,
    TypeRegistry,
    Device,
)

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Device)
def create_device_verification(sender, instance, created, **kwargs):
    if created:
        Verification.objects.create(
            device=instance,
            org_title="ручной ввод",
            valid_date=instance.valid_date,
            is_actual=True,
        )


@receiver(post_save, sender=Verification)
def refresh_device_data(sender, instance, created, **kwargs):
    if instance.is_actual and not created:
        with transaction.atomic():
            for verification in Verification.objects.filter(device=instance.device):
                verification.is_actual = False
                verification.save()
            instance.is_actual = True
            # device = instance.device
            # if instance.mit_number:
            #     device_registry_number = RegistryNumber.objects.get_or_create(
            #         registry_number=instance.mit_number
            #     )[0]
            #     instance.device.registry_number = device_registry_number
            # if instance.mit_notation:
            #     device_type = TypeName.objects.get_or_create(
            #         type=instance.mit_notation
            #     )[0]
            #     instance.device.type = device_type
            # if instance.mi_modification:
            #     device_modification = Modification.objects.get_or_create(
            #         modification=instance.mi_modification, type=instance.device.type
            #     )[0]
            #     instance.device.modification = device_modification
            # if instance.mit_number and instance.mit_notation:
            #     TypeRegistry.objects.get_or_create(
            #         type=device_type, number_registry=device_registry_number
            #     )
            # instance.device.save()
