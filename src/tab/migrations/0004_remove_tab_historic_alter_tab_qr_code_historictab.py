# Generated by Django 5.0 on 2024-01-27 02:44

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0008_alter_order_tab'),
        ('tab', '0003_tab_historic_alter_tab_qr_code'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tab',
            name='historic',
        ),
        migrations.AlterField(
            model_name='tab',
            name='qr_code',
            field=models.ImageField(blank=True, editable=False, upload_to='qr_codes'),
        ),
        migrations.CreateModel(
            name='HistoricTab',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('client', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('order', models.ManyToManyField(editable=False, to='order.order')),
            ],
        ),
    ]
