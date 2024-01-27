from uuid import uuid4
from decimal import Decimal
from django.db import models

from cart.models import Cart
from order.models import Order
from restaurant.models import Food


# Create your models here.
class Item(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    food = models.ForeignKey(Food, on_delete=models.PROTECT)
    quantity = models.IntegerField(default=1)
    price: Decimal = models.DecimalField(
                                            max_digits=6,
                                            decimal_places=2,
                                            default=0.00 # type: ignore
                                        )

    def get_price(self) -> Decimal:
        return self.price

    def get_total_price(self) -> Decimal:
        return self.quantity * self.price
