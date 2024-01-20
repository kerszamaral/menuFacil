from io import BytesIO
from uuid import uuid4
from django.db import models
from django.urls import reverse
import qrcode
from PIL import Image
from django.core.files import File

from menuFacil import settings

class Tab(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True, editable=False)
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        editable=False,
    )

    def save(self, *args, **kwargs):
        link = reverse('order:confirm_order', args=[self.id])#Arrumar URL
        qr_image = qrcode.make(link)
        canvas = Image.new('RGB', (380, 380), color='white')
        canvas.paste(qr_image)
        file_name = f'qr_code_{self.id}.png'
        stream = BytesIO()
        canvas.save(stream, 'PNG')
        self.qr_code.save(file_name, File(stream), save=False)
        canvas.close()
        super().save(*args, **kwargs)
