from uuid import uuid4
from django.db import models

from django.conf import settings
from django.http import HttpRequest

from restaurant.models import Food
from validation import CART_KEY, cart_token_exists

# Create your models here.
class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True)

    def get_length(request: HttpRequest) -> int:
        if cart_token_exists(request):
            cart = Cart.objects.get(id=request.session[CART_KEY])
            return sum(item.quantity for item in Item.objects.filter(cart=cart))
        return 0

class Item(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
