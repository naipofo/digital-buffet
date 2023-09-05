from django.http import Http404
from django.shortcuts import redirect, render

from .models import FoodOffer


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
    cart = request.session["cart"]

    products = FoodOffer.objects.filter(id__in=cart.keys())

    total_price = 0
    display_cart = []

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

    context = {"cart": display_cart, "total": total_price / 100}
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
    return render(request, "frontbuffet/receipt.html", {})
