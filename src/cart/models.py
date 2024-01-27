from uuid import uuid4
from django.db import models

from django.contrib.auth.models import AbstractBaseUser, AnonymousUser
from django.contrib.sessions.backends.base import SessionBase
from django.conf import settings
from restaurant.models import Restaurant

CART_KEY = 'cart_token'

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
        return sum(item.get_total_price() for item in self.item_set.all()) # type: ignore


def get_cart_length(session: SessionBase, user: AbstractBaseUser | AnonymousUser) -> int:
    if user.is_authenticated:
        session[CART_KEY] = str(user.cart.id) # type: ignore

    (cart, created)= Cart.objects.get_or_create(id=session.get(CART_KEY, None),
                        defaults={'client': user if user.is_authenticated else None}
                    )
    if created:
        session[CART_KEY] = str(cart.id)
    return cart.get_length()

