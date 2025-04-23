from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from social_django.models import UserSocialAuth


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    telegram_id = models.PositiveIntegerField(null=True, blank=True)

    @property
    def full_name(self) -> str:
        if self.user.first_name and self.user.last_name:
            return f"{self.user.first_name} {self.user.last_name}"
        return self.user.first_name or self.user.last_name

    def __str__(self) -> str:
        return str(self.user)


# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
