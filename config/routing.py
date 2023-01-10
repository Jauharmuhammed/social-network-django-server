from django.urls import path
from apps.chats.consumers import ChatConsumer, NotificationConsumer

websocket_urlpatterns = [
    path("chats/<conversation_name>/", ChatConsumer.as_asgi()),
    path("notifications/chat/", NotificationConsumer.as_asgi()),
]
