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

    @property
    def is_online(self):
        return self.last_action_dt and timezone.now() - self.last_action_dt > \
               datetime.timedelta(minutes=ONLINE_TIMEOUT_SEC)

    # def block_token(self, token):
    #     payload = jwt_decode_handler(token)
    #     expired_dt = datetime.fromtimestamp(payload['exp'], tz=timezone.get_current_timezone())
    #
    #     if expired_dt <= timezone.now():
    #         # Already expired
    #         return
    #
    #     self.blocked_tokens.get_or_create(token=token, defaults={
    #         'expired_dt': expired_dt
    #     })
