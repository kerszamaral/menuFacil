from uuid import uuid4
from django.db import models

from django.contrib.auth.models import AbstractBaseUser, AnonymousUser
from django.contrib.sessions.backends.base import SessionBase
from django.conf import settings
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
        return sum(item.get_total_item_price() for item in self.item_set.all()) # type: ignore


def get_cart_length(session: SessionBase, user: AbstractBaseUser | AnonymousUser) -> int:
    if not cart_token_exists(session, user):
        return 0

    cart = Cart.objects.get(id=session[CART_KEY])
    return cart.get_length()

def get_cart_total_price(session: SessionBase, user: AbstractBaseUser | AnonymousUser) -> float:
    if not cart_token_exists(session, user):
        return 0

    cart = Cart.objects.get(id=session[CART_KEY])
    return cart.get_total_price()
