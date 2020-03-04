from django.conf import settings
from django.db import models


class Room(models.Model):
    title = models.TextField()
    last_message = models.ForeignKey('rooms.Message', on_delete=models.SET_NULL, null=True, related_name='+')

    def __str__(self):
        return self.title


class Message(models.Model):
    room = models.ForeignKey('rooms.Room', on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    created_dt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}: {}...'.format(self.owner, self.message[:100])


class Notification(models.Model):
    room = models.ForeignKey('rooms.Room', on_delete=models.CASCADE)
    message = models.TextField()
    created_dt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}: {}...'.format(self.room, self.message[:100])
