from django.db import models
from django.conf import settings
from uuid import uuid4

from restaurant.models import Food, Restaurant

# Create your models here.
class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class StatusType(models.TextChoices):
        """Enums for the types of Food possible."""
        OPEN = "OP", "Open"
        PENDING = "PD", "Pending"
        ACCEPTED = "AC", "Accepted"
        REJECTED = "RJ", "Rejected"
        DELIVERED = "DV", "Delivered"
        CANCELLED = "CL", "Cancelled"
        
    status = models.CharField(
        max_length=2,
        choices=StatusType.choices,
        default=StatusType.OPEN,
    )
    
    def __str__(self):
        return f'{self.client.username} - {self.restaurant.name} - {self.total_price} - {self.created_at}'

class Item(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    def __str__(self):
        return f'{self.food} x{self.quantity}'