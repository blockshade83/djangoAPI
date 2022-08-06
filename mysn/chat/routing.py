from django.urls import path, re_path
from . import consumers

print('routing.py module called')
websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
]