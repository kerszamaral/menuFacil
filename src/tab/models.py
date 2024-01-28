from uuid import uuid4
from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation

from restaurant.models import Restaurant
from order.models import Order

class AbstractTab(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    client = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        editable=False,
        null=True,
    )
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.SET_NULL,
        editable=False,
        null=True,
    )
    order = GenericRelation(
        Order,
        content_type_field="tab_type",
        object_id_field="tab_id"
    )

    class Meta:
        abstract = True

    def get_total_price(self) -> float:
        return sum(order.get_total_price() for order in self.order.all())

class Tab(AbstractTab):
    def __str__(self) -> str:
        return str(self.id).split('-')[0]

class HistoricTab(AbstractTab):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        editable=False,
        null=True,
    )
