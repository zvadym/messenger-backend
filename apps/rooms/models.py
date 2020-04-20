from django.conf import settings
from django.db import models
from django.dispatch import receiver


class Room(models.Model):
    title = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='+', blank=True)
    last_message = models.ForeignKey(
        'rooms.Message',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+'
    )
    created_dt = models.DateTimeField(auto_now_add=True)
    is_private = models.BooleanField(default=False)

    class Meta:
        ordering = ['-last_message__created_dt', '-created_dt']

    def __str__(self):
        return self.title

    @property
    def updated_dt(self):
        return self.last_message.created_dt if self.last_message else self.created_dt


class Message(models.Model):
    room = models.ForeignKey('rooms.Room', on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    created_dt = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_dt']

    def __str__(self):
        return '{}: {}...'.format(self.created_by, self.message[:100])


class Notification(models.Model):
    room = models.ForeignKey('rooms.Room', on_delete=models.CASCADE)
    message = models.TextField()
    created_dt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}: {}...'.format(self.room, self.message[:100])


@receiver(models.signals.post_save, sender=Message)
def message_created(sender, instance, created, **kwargs):
    if created:
        instance.room.last_message = instance
        instance.room.save()
