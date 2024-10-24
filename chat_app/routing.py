from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/chat_app/<str:channel_name>/', consumers.ChatConsumer.as_asgi()),
]
