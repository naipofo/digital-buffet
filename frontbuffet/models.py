from django.db import models


class FoodOffer(models.Model):
    title = models.CharField(max_length=200)
    image = models.URLField()
    price = models.IntegerField()


class PlacedOrder(models.Model):
    order_code = models.CharField(max_length=4)

    def __str__(self):
        return f"Order: " + ", ".join(str(x) for x in self.orderentry_set.all())


class OrderEntry(models.Model):
    order = models.ForeignKey(PlacedOrder, on_delete=models.CASCADE)
    product = models.ForeignKey(FoodOffer, on_delete=models.CASCADE)
    amount = models.IntegerField()

    def __str__(self):
        return self.product.title
