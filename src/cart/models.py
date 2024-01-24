from uuid import uuid4
from django.db import models

from django.conf import settings
from django.http import HttpRequest
from restaurant.models import Restaurant

from menuFacil.validation import CART_KEY, cart_token_exists

# Create your models here.
class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    client = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True, null=True
    )
    restaurant = models.ForeignKey(
            Restaurant,
            on_delete=models.SET_NULL,
            null=True
        )

    def get_length(self) -> int:
        return sum(item.quantity for item in self.item_set.all()) # type: ignore

    def get_total_price(self) -> float:
        return sum(item.price for item in self.item_set.all()) # type: ignore


def get_cart_length(request: HttpRequest) -> int:
    if not cart_token_exists(request):
        return 0

    cart = Cart.objects.get(id=request.session[CART_KEY])
    return cart.get_length()

def get_cart_total_price(request: HttpRequest) -> float:
    if not cart_token_exists(request):
        return 0

    cart = Cart.objects.get(id=request.session[CART_KEY])
    return cart.get_total_price()
