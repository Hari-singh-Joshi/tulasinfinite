from django.urls import re_path
from .patient import VideoCallConsumer

websocket_urlpatterns = [
    re_path(r'ws/video/(?P<room_name>\w+)/$', VideoCallConsumer.as_asgi()),
]