import datetime
import channels.layers
from asgiref.sync import async_to_sync
from django.db.models import signals
from django.dispatch import receiver
from django.utils import timezone

from apps.api.serializers import MessageSerializer, NotificationSerializer, RoomSerializer, UserSerializer
from apps.members.models import User
from apps.rooms.models import Room, Message, Notification

from .consumers import MessengerConsumer


def get_active_members():
    return User.objects.filter(last_action_dt__gte=timezone.now() - datetime.timedelta(hours=1))


@receiver(signals.post_save, sender=Room)
def room_observer(sender, instance, created, **kwargs):
    layer = channels.layers.get_channel_layer()

    def _send(group_name):
        async_to_sync(layer.group_send)(group_name, {
            'type': 'websocket.room',
            'data': {
                'created': created,
                'instance_data': RoomSerializer(instance).data,
            }
        })

    if instance.is_private:
        members = list(instance.members.all())
        members.append(instance.created_by)
    else:
        members = get_active_members()

    group_template = MessengerConsumer.GROUPS['my' if created else 'member']

    # TODO: members -> find diff and unsubscribe deleted members / subscribe the new ones
    for member in members:
        _send(group_template.format(member_id=member.id))


@receiver(signals.m2m_changed, sender=Room.members.through)
def room_members_observer(sender, instance, action, pk_set, **kwargs):
    # TODO: `room_observer` doesnt handle the members field changes
    #  so it should be done here
    if action == 'post_remove':
        print('room_members_observer - deleted', instance, pk_set)
    if action == 'post_add':
        print('room_members_observer - added', instance, pk_set)


@receiver(signals.post_save, sender=Message)
def message_observer(sender, instance, created, **kwargs):
    if not created:
        # TODO: handle updated (edited) messages
        return

    layer = channels.layers.get_channel_layer()
    room = instance.room

    async_to_sync(layer.group_send)(
        MessengerConsumer.GROUPS['room'].format(room_id=room.id),
        {
            'type': 'websocket.message',
            'data': {
                'created': created,
                'instance_data': MessageSerializer(instance).data,
            }
        }
    )


@receiver(signals.post_save, sender=Notification)
def notification_observer(sender, instance, created, **kwargs):
    if not created:
        return

    layer = channels.layers.get_channel_layer()
    room = instance.room

    async_to_sync(layer.group_send)(
        MessengerConsumer.GROUPS['room'].format(room_id=room.id),
        {
            'type': 'websocket.notification',
            'data': NotificationSerializer(instance).data,
        }
    )


@receiver(signals.post_save, sender=User)
def member_observer(sender, instance, created, **kwargs):
    layer = channels.layers.get_channel_layer()

    def _send(group_name):
        async_to_sync(layer.group_send)(
            group_name,
            {
                'type': 'websocket.member',
                'data': {
                    'created': created,
                    'instance_data': UserSerializer(instance).data,
                }
            }
        )

    if created:
        # Find all active members and send them a notification about a new member
        for user in get_active_members():
            _send(MessengerConsumer.GROUPS['my'].format(member_id=user.id))

    else:
        _send(MessengerConsumer.GROUPS['member'].format(member_id=instance.id))
