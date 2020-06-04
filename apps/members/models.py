import datetime
from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.db import models
from django.utils import timezone


ONLINE_TIMEOUT_SEC = 5 * 60


class User(AbstractUser):
    last_action_dt = models.DateTimeField(auto_now=True)

    username_validator = validators.EmailValidator()

    def save(self, *args, **kwargs):
        # self.username = self.email  # doesn't work from "admin"
        super().save(*args, **kwargs)

    def update_last_action_dt(self):
        self.last_action_dt = timezone.now()
        self.save(update_fields=['last_action_dt'])

    @property
    def is_online(self):
        return self.last_action_dt and timezone.now() - self.last_action_dt < \
               datetime.timedelta(minutes=ONLINE_TIMEOUT_SEC)
