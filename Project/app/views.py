from django.shortcuts import render
from django.urls import reverse
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Dish
from .serializers import DishSerializer
from rest_framework import viewsets

class DishViewSet(viewsets.ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer

    @action(detail=True, methods=['patch'])
    def toggle_published(self, request, pk=None):
        dish = self.get_object()
        dish.isPublished = not dish.isPublished
        dish.save()

        # Send WebSocket update
        from channels.layers import get_channel_layer
        from asgiref.sync import async_to_sync

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "dishes",
            {
                "type": "dish_message",
                "message": {
                    "dishId": dish.dishId,
                    "isPublished": dish.isPublished
                }
            }
        )

        return Response({'dishId': dish.dishId, 'isPublished': dish.isPublished})

def dashboard(request):
    dishes = Dish.objects.all()
    return render(request, 'dashboard.html', {'dishes': dishes})
