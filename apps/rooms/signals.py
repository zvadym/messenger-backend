from django.db.models import signals
from django.dispatch import receiver
from .models import Room, Notification, Message


@receiver(signals.post_save, sender=Message)
def message_created(sender, instance, created, **kwargs):
    if created:
        instance.room.last_message = instance
        instance.room.save()


@receiver(signals.post_save, sender=Room)
def room_created_notifications(sender, instance, created, **kwargs):
    if not created:
        return

    Notification.objects.create(
        room=instance,
        message='Room is created by {}'.format(instance.created_by)
    )


@receiver(signals.pre_save, sender=Room)
def room_changed_notifications(sender, instance, **kwargs):
    try:
        prev_instance = Room.objects.get(pk=instance.pk)
    except Room.DoesNotExist:
        return

    if prev_instance.title != instance.title:
        Notification.objects.create(
            room=instance,
            message='Title is changed from "{}" to "{}"'.format(
                prev_instance.title,
                instance.title
            )
        )

    if prev_instance.is_private != instance.is_private:
        Notification.objects.create(
            room=instance,
            message='Room is become {}'.format('private' if instance.is_private else 'public')
        )
