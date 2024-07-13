from django.db import models

class Dish(models.Model):
    dishId = models.CharField(max_length=10, unique=True, primary_key=True)
    dishName = models.CharField(max_length=100)
    imageUrl = models.URLField(max_length=255)
    isPublished = models.BooleanField(default=True)
    
    def __str__(self):
        return self.dishName
