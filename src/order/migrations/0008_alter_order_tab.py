# Generated by Django 5.0 on 2024-01-24 22:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0007_remove_order_payed_alter_order_restaurant_and_more'),
        ('tab', '0002_alter_tab_client'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='tab',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='tab.tab'),
        ),
    ]