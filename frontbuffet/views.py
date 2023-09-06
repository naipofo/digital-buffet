import random
import string
from django.http import Http404
from django.shortcuts import redirect, render

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
    cart = request.session.get("cart", {})

    if offer_id not in cart:
        cart[offer_id] = {"quantity": 1}
    else:
        cart[offer_id]["quantity"] += 1

    request.session["cart"] = cart

    return redirect("cart")


def cart(request):
    cart = request.session.get("cart", {})

    if len(cart) == 0:
        return redirect("empty_cart")

    cart = display_cart(request)

    context = {"cart": cart[1], "total": cart[0] / 100}
    return render(request, "frontbuffet/cart.html", context)


def checkout(request):
    cart = request.session["cart"]
    products = FoodOffer.objects.filter(id__in=cart.keys())
    total_price = 0
    orders = []

    for item in cart.items():
        product = products.get(id=item[0])
        quantity = item[1]["quantity"]
        total_price += quantity * product.price
        if item[1]["quantity"] > 1:
            orders += [f"{quantity}x {product.title}"]
        else:
            orders += [product.title]

    return render(
        request,
        "frontbuffet/checkout.html",
        {"total": total_price / 100, "order_string": ",".join(orders)},
    )


def receipt(request):
    cart = request.session["cart"]

    order_code = "".join(random.choice(string.digits) for _ in range(6))
    order = PlacedOrder(order_code=order_code)
    order.save()

    formated_cart = display_cart(request)

    for item in cart.items():
        entry = OrderEntry(
            order=order,
            product=FoodOffer.objects.get(pk=item[0]),
            amount=item[1]["quantity"],
        )
        entry.save()

    request.session["cart"] = {}

    orders = request.session.get("orders", [])
    orders += [order.id]
    request.session["orders"] = orders

    return render(
        request,
        "frontbuffet/receipt.html",
        {"cart": formated_cart[1], "total": formated_cart[0] / 100, "code": order_code},
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
    if order.order_code != str(code):
        return Http404("Order not found")

    return render(
        request,
        "frontbuffet/order.html",
        {"order": order},
    )


def display_cart(request) -> [int, list[dict]]:
    cart = request.session["cart"]
    products = FoodOffer.objects.filter(id__in=cart.keys())
    total_price = 0
    display_cart = []
    orders = []

    for item in cart.items():
        product = products.get(id=item[0])
        price = item[1]["quantity"] * product.price
        total_price += price
        display_cart += [
            {
                "product": product,
                "quantity": item[1]["quantity"],
                "total_price": price / 100,
            }
        ]

    return (total_price, display_cart)
