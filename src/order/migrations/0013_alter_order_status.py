# Generated by Django 5.0.1 on 2024-01-28 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0012_remove_order_total_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('MD', 'Made'), ('IP', 'In Progress'), ('DV', 'Delivered'), ('CL', 'Cancelled')], default='MD', max_length=2),
        ),
    ]