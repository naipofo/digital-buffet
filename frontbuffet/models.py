from django.db import models

class FoodOffer(models.Model):
    title = models.CharField(max_length=200)
    image = models.URLField()
    price = models.IntegerField()
