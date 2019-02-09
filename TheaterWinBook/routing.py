# chat/routing.py
from django.conf.urls import url
from . import consumers
from django.conf.urls import include


websocket_urlpatterns = [
    url(r'^ws/chatting_room/(?P<room_name>[^/]+)/$', consumers.ChatConsumer),
]



