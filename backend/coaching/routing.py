from django.urls import path
from channels.routing import URLRouter
from . import consumers

websocket_urlpatterns = [
    path('ws/coaching/<int:session_id>/', consumers.CoachingConsumer.as_asgi()),
]
