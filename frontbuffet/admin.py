from django.contrib import admin

from .models import FoodOffer, OrderEntry, PlacedOrder

admin.site.register(FoodOffer)
admin.site.register(OrderEntry)
admin.site.register(PlacedOrder)
