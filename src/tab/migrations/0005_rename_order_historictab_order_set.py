# Generated by Django 5.0 on 2024-01-27 02:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tab', '0004_remove_tab_historic_alter_tab_qr_code_historictab'),
    ]

    operations = [
        migrations.RenameField(
            model_name='historictab',
            old_name='order',
            new_name='order_set',
        ),
    ]
