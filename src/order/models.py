from uuid import uuid4
from django.db import models
from django.conf import settings
from django.urls import reverse

import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image

from restaurant.models import Food, Restaurant

# Create your models here.
class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        editable=False,
    )
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, editable=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True, editable=False)
    pending_cancellation = models.BooleanField(default=False)
    payed = models.BooleanField(default=False)
    
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
    
    def __str__(self):
        return f'{self.client.username} - {self.total_price} - {self.created_at.strftime(" %H:%M %d/%m/%Y")}'
    
    def save(self, *args, **kwargs):
        link = reverse('order:confirm_order', args=[self.id])
        qr_image = qrcode.make(link)
        canvas = Image.new('RGB', (380, 380), color='white')
        canvas.paste(qr_image)
        file_name = f'qr_code_{self.id}.png'
        stream = BytesIO()
        canvas.save(stream, 'PNG')
        self.qr_code.save(file_name, File(stream), save=False)
        canvas.close()
        super().save(*args, **kwargs)
    
class Item(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)