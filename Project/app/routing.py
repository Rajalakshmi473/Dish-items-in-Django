from django.urls import re_path
from app.consumers import DishConsumer

websocket_urlpatterns = [
    re_path(r'ws/dishes/$', DishConsumer.as_asgi()),
]
