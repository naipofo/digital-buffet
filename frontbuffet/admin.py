from django.contrib import admin

from .models import FoodOffer, OrderEntry, PlacedOrder, FoodTag

admin.site.register(FoodOffer)
admin.site.register(FoodTag)
admin.site.register(OrderEntry)
admin.site.register(PlacedOrder)
