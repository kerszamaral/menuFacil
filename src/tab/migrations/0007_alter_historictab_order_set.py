# Generated by Django 5.0 on 2024-01-27 03:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0010_alter_order_tab'),
        ('tab', '0006_alter_historictab_order_set'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historictab',
            name='order_set',
            field=models.ManyToManyField(editable=False, to='order.order'),
        ),
    ]
