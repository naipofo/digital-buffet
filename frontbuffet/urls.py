from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:offer_id>", views.detail, name="detail"),
    path("cart", views.cart, name="cart"),
    path("add-to-cart/<int:offer_id>", views.add_to_cart, name="add_to_cart"),
]
