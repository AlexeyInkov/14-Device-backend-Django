from django.conf import settings
from django.db import models
from social_django.models import UserSocialAuth

from apps.device.models import Organization, UserToOrganization


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
