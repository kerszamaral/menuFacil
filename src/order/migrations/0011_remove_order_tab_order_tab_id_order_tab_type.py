# Generated by Django 5.0.1 on 2024-01-27 14:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('order', '0010_alter_order_tab'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='tab',
        ),
        migrations.AddField(
            model_name='order',
            name='tab_id',
            field=models.UUIDField(editable=False, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='tab_type',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.contenttype'),
        ),
    ]