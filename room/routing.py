from django.urls import re_path
from django.conf.urls import url

from .consumers import ChatConsumer

websocket_urlpatterns = [
    re_path(r'^ws/chat/(?P<room_name>\d+)/$', ChatConsumer.as_asgi()),
]
