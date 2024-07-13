import json
import os
from django.core.management.base import BaseCommand
from app.models import Dish  

class Command(BaseCommand):
    help = 'Load dishes from a JSON file'

    def handle(self, *args, **kwargs):
        print("Command is being executed") 
        file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'fixtures', 'dishes.json')
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'File {file_path} does not exist'))
            return

        with open(file_path, 'r') as file:
            data = json.load(file)
            for item in data:
                Dish.objects.update_or_create(
                    dishId=item['dishId'],
                    defaults={
                        'dishName': item['dishName'],
                        'imageUrl': item['imageUrl'],
                        'isPublished': item['isPublished']
                    }
                )
        self.stdout.write(self.style.SUCCESS('Successfully loaded dishes data'))
