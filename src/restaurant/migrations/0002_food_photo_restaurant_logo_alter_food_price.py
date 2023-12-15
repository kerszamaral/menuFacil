# Generated by Django 5.0 on 2023-12-15 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='food',
            name='photo',
            field=models.ImageField(blank=True, upload_to='food_photos'),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='logo',
            field=models.ImageField(blank=True, upload_to='restaurant_logos'),
        ),
        migrations.AlterField(
            model_name='food',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
    ]