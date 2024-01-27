from io import BytesIO
from uuid import uuid4
from django.db import models
from django.core.files import File
from django.conf import settings
import qrcode
from PIL import Image

from restaurant.models import Restaurant

class Tab(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True, editable=False)
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

    def save(self, *args, **kwargs):
        qr_image = qrcode.make(self.id)
        canvas = Image.new('RGB', (380, 380), color='white')
        canvas.paste(qr_image)
        file_name = f'qr_code_{self.id}.png'
        stream = BytesIO()
        canvas.save(stream, 'PNG')
        self.qr_code.save(file_name, File(stream), save=False) # pylint: disable=E1101
        canvas.close()
        return super().save(*args, **kwargs)

class HistoricTab(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        editable=False,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    order_set = models.ManyToManyField(
        'order.Order',
        editable=False
    )
