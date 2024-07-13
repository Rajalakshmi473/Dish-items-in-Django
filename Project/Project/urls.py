from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app.views import DishViewSet, dashboard

router = DefaultRouter()
router.register(r'dishes', DishViewSet, basename='dish')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('', dashboard, name='dashboard'),
    path('toggle_published/<int:dishId>/', DishViewSet.as_view({'patch': 'toggle_published'}), name='toggle_published'),
]

# Add this if you want to serve WebSocket URLs from the same file
from django.urls import re_path
from app.consumers import DishConsumer

websocket_urlpatterns = [
    re_path(r'ws/dishes/$', DishConsumer.as_asgi()),
]
