# Generated by Django 5.0 on 2023-12-15 19:10

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0002_food_photo_restaurant_logo_alter_food_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
