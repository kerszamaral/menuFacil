from uuid import uuid4
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from restaurant.models import Restaurant

class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.SET_NULL, editable=False, null=True)

    tab_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, editable=False, null=True)
    tab_id = models.UUIDField(editable=False, null=True)
    tab = GenericForeignKey('tab_type', 'tab_id')

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    pending_cancellation = models.BooleanField(default=False)

    class StatusType(models.TextChoices):
        MADE = ("MD", "Made")
        IN_PROGRESS = ("IP", "In Progress")
        DELIVERED = ("DV", "Delivered")
        CANCELLED = ("CL", "Cancelled")

        def __str__(self):
            return self.label

    status = models.CharField(
        max_length=2,
        choices=StatusType.choices,
        default=StatusType.MADE,
    )

    def get_length(self) -> int:
        return sum(item.quantity for item in self.item_set.all()) # type: ignore

    def get_total_price(self) -> float:
        return sum(item.get_total_price() for item in self.item_set.all()) # type: ignore

    def __str__(self):
        return f'{self.get_total_price()} - {self.created_at.strftime(" %H:%M %d/%m/%Y")}'  # pylint: disable=maybe-no-member # type: ignore
