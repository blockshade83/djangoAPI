from django.urls import include, path
from . import views
from django.conf.urls import url
from . import consumers
from . import routing

urlpatterns = [
    path('<str:room_name>/', views.room, name = 'room'),
    # path('ws/room1/', consumers.ChatConsumer.as_asgi()),
]