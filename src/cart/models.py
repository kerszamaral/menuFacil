from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AnonymousUser

from django.conf import settings

from restaurant.models import Food

# Create your models here.
class Cart(models.Model):
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    def __str__(self) -> str:
        return f'{self.quantity} x {self.food}'
    
    def get_cart_length(user: AbstractBaseUser | AnonymousUser) -> int:
        cart = Cart.objects.filter(client=user)
        return sum(item.quantity for item in cart)
