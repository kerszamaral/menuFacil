from uuid import uuid4
from django.db import models
from restaurant.models import Restaurant
from tab.models import Tab

class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.SET_NULL, editable=False, null=True)
    tab = models.ForeignKey(Tab, on_delete=models.CASCADE, editable=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    pending_cancellation = models.BooleanField(default=False)

    class StatusType(models.TextChoices):
        OPEN = ("OP", "Open")
        MADE = ("MD", "Made")
        IN_PROGRESS = ("IP", "In Progress")
        DELIVERED = ("DV", "Delivered")
        CANCELLED = ("CL", "Cancelled")

        def __str__(self):
            return self.label

    status = models.CharField(
        max_length=2,
        choices=StatusType.choices,
        default=StatusType.OPEN,
    )

    def get_length(self) -> int:
        return sum(item.quantity for item in self.item_set.all()) # type: ignore

    def get_total_price(self) -> float:
        return sum(item.get_total_item_price() for item in self.item_set.all()) # type: ignore

    def __str__(self):
        return f'{self.tab.id} - {self.total_price} - {self.created_at.strftime(" %H:%M %d/%m/%Y")}'  # pylint: disable=maybe-no-member
