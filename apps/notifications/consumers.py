from channels.generic.websocket import JsonWebsocketConsumer
import json
from asgiref.sync import async_to_sync
from .models import Notification
from uuid import UUID



class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return obj.hex
        return json.JSONEncoder.default(self, obj)


class NotificationsConsumer(JsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user = None
        self.notification_group_name = None


    def connect(self):
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            return

        self.accept()

        # private notification group
        self.notification_group_name = self.user.username + "__notifications"
        async_to_sync(self.channel_layer.group_add)(
            self.notification_group_name,
            self.channel_name,
        )

        # Send count of unread notificatios
        unread_count = Notification.objects.filter(to_user=self.user, read=False).count()
        self.send_json(
            {
                "type": "unread_count",
                "unread_count": unread_count,
            }
        )




    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.notification_group_name,
            self.channel_name,
        )
        return super().disconnect(close_code)

    def receive_json(self, content, **kwargs):
        print(content)
        message_type = content["type"]
        print('message recieved')

        if message_type == "read_notifications":
            notification_to_me = Notification.objects.filter(to_user=self.user)
            notification_to_me.update(read=True)

            # Update the unread message count
            unread_count = Notification.objects.filter(to_user=self.user, read=False).count()
            async_to_sync(self.channel_layer.group_send)(
                self.user.username + "__notifications",
                {
                    "type": "unread_count",
                    "unread_count": unread_count,
                },
            )

    def unread_count(self, event):
        self.send_json(event)


    def new_notification(self,event):
        print('Event Triggered')
        # Receive message from room group
        message = event['message']
        # Send message to WebSocket
        self.send_json(event)

    @classmethod
    def encode_json(cls, content):
        return json.dumps(content, cls=UUIDEncoder)