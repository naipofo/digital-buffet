from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:offer_id>", views.detail, name="detail"),
    path("cart", views.cart, name="cart"),
    path("add-to-cart/<int:offer_id>", views.add_to_cart, name="add_to_cart"),
    path("checkout", views.checkout, name="checkout"),
    path("receipt", views.receipt, name="receipt"),
    path("empty_cart", views.empty_cart, name="empty_cart"),
    path("orders", views.orders, name="orders"),
]
