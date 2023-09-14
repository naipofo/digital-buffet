import json

from frontbuffet.models import FoodOffer
from pydantic import BaseModel


class ShoppingCartEntry(BaseModel):
    product_id: int
    amount: int

    @property
    def product(self):
        return FoodOffer.objects.get(id=self.product_id)

    @property
    def value(self):
        return self.product.price * self.amount / 100


class Cart(BaseModel):
    items: list[ShoppingCartEntry]

    @property
    def value(self):
        return sum(x.value for x in self.items)


def clear_shopping_cart(session):
    save_shopping_cart(session, Cart(items=[]))


def save_shopping_cart(session, cart: Cart):
    session["shopping_cart"] = cart.model_dump_json()


def get_shopping_cart(session):
    shopping_cart_json = session.get("shopping_cart", "")
    if len(shopping_cart_json) == 0:
        clear_shopping_cart(session)
        return get_shopping_cart(session)

    return Cart(**json.loads(shopping_cart_json))


def add_to_shopping_cart(session, product_id, amount):
    shopping_cart = get_shopping_cart(session)

    found = False
    for entry in shopping_cart.items:
        if entry.product_id == product_id:
            entry.amount += amount
            found = True
            break

    if not found:
        shopping_cart.items.append(
            ShoppingCartEntry(product_id=product_id, amount=amount)
        )

    save_shopping_cart(session, shopping_cart)
