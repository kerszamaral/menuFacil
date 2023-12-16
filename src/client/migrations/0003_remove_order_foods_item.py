# Generated by Django 5.0 on 2023-12-16 01:31

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0002_alter_order_id_alter_order_status'),
        ('restaurant', '0009_food_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='foods',
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('quantity', models.IntegerField(default=1)),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant.food')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.order')),
            ],
        ),
    ]
