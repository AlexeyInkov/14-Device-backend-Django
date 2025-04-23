import logging

from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from social_django.models import UserSocialAuth

from apps.device.models import Organization, UserToOrganization
from apps.my_auth.models import Profile

logger = logging.getLogger(__name__)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        logger.info(f"Profile created for user {instance}")


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=UserSocialAuth)
def add_telegram_id_into_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.get(user=instance.user)
        profile.telegram_id = instance.uid
        logger.info(f"Telegram ID added to profile: {profile}")
        profile.save()


@receiver(post_save, sender=User)
def add_organizations_in_user_admin(sender, instance, **kwargs):
    if instance.is_superuser or instance.is_staff:
        for organization in Organization.objects.all():
            _, added = UserToOrganization.objects.get_or_create(
                user=instance, organization=organization
            )
            if added:
                logger.info(f"{instance} add {organization}")
