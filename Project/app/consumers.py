# app/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class DishConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            "dishes",
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            "dishes",
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        dish_id = text_data_json['dishId']
        is_published = text_data_json['isPublished']

        # Update the status in the database
        dish = await database_sync_to_async(Dish.objects.get)(dishId=dish_id)
        dish.isPublished = is_published
        await database_sync_to_async(dish.save)()

        # Broadcast the change to all connected clients
        await self.channel_layer.group_send(
            "dishes",
            {
                'type': 'dish_message',
                'dishId': dish_id,
                'isPublished': is_published
            }
        )

    async def dish_message(self, event):
        dish_id = event['dishId']
        is_published = event['isPublished']

        await self.send(text_data=json.dumps({
            'dishId': dish_id,
            'isPublished': is_published
        }))
