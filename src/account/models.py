from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings

from cart.models import Cart
from tab.models import Tab

# Create your models here.
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_fields(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(client=instance)
        Tab.objects.create(client=instance)
        instance.cart.save()
        instance.tab.save()
