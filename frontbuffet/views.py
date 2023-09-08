import random
import string
from django.http import Http404
from django.shortcuts import redirect, render

from frontbuffet.shopping_cart import (
    add_to_shopping_cart,
    clear_shopping_cart,
    get_shopping_cart,
)

from .models import FoodOffer, OrderEntry, PlacedOrder


def index(request):
    latest_question_list = FoodOffer.objects.all()
    return render(
        request,
        "frontbuffet/index.html",
        {
            "all_offers_list": latest_question_list,
        },
    )


def detail(request, offer_id):
    try:
        offer = FoodOffer.objects.get(pk=offer_id)
    except FoodOffer.DoesNotExist:
        raise Http404("Offer does not exist")
    return render(request, "frontbuffet/detail.html", {"offer": offer})


def add_to_cart(request, offer_id):
    add_to_shopping_cart(request.session, offer_id, 1)
    return redirect("cart")


def cart(request):
    cart = get_shopping_cart(request.session)

    if len(cart.items) == 0:
        return redirect("empty_cart")

    context = {"cart": cart}
    return render(request, "frontbuffet/cart.html", context)


def checkout(request):
    cart = get_shopping_cart(request.session)

    return render(
        request,
        "frontbuffet/checkout.html",
        {"cart": cart},
    )


def receipt(request):
    cart = get_shopping_cart(request.session)

    order_code = "".join(random.choice(string.digits) for _ in range(6))
    order = PlacedOrder(order_code=order_code)
    order.save()

    for item in cart.items:
        entry = OrderEntry(
            order=order,
            product=FoodOffer.objects.get(pk=item.product_id),
            amount=item.amount,
        )
        entry.save()

    orders = request.session.get("orders", [])
    orders += [order.id]
    request.session["orders"] = orders

    clear_shopping_cart(request.session)

    return render(
        request,
        "frontbuffet/receipt.html",
        {"cart": cart, "code": order_code},
    )


def empty_cart(request):
    return render(request, "frontbuffet/empty_cart.html", {})


def orders(request):
    orders = request.session.get("orders", [])
    return render(
        request,
        "frontbuffet/orders.html",
        {"orders": PlacedOrder.objects.filter(id__in=orders)},
    )


def order(request, id, code):
    order = PlacedOrder.objects.get(pk=id)
    print(order.order_code)
    if order.order_code != code:
        return Http404("Order not found")

    return render(
        request,
        "frontbuffet/order.html",
        {"order": order, "items": order.orderentry_set.all()},
    )
