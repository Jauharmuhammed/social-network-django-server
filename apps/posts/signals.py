from django.db.models.signals import post_save
from .models import Comment
from django.dispatch import receiver

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from apps.notifications.models import Notification
from apps.notifications.serializers import NotificationSerializer

@receiver(post_save, sender=Comment)
def create_comment(sender, instance, created, **kwargs):
    if created:

        if instance.parent:
            if instance.user == instance.parent.user: return

            # create a new reply notification
            notification = Notification.objects.create(
                to_user = instance.parent.user,
                created_by = instance.user,
                content = f'Replied to your comment: {instance.body}',
                notification_type = 'reply',
                post = instance.post,
            )

            # send notification to the user
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f'{instance.parent.user.username}__notifications',
                {
                    'type': 'new_notification',
                    'message': NotificationSerializer(notification).data
                }
            )
            print(instance.parent.user.username)
        else:
            if instance.user == instance.post.user: return

            # create a new comment notification
            notification = Notification.objects.create(
                to_user = instance.post.user,
                created_by = instance.user,
                content = f'Commented on your post: {instance.body}',
                notification_type = 'comment',
                post = instance.post,
            )

            # send notification to the user
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f'{instance.post.user.username}__notifications',
                {
                    'type': 'new_notification',
                    'message': NotificationSerializer(notification).data
                }
            )

        
