# Generated by Django 4.0.2 on 2022-06-11 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jp_app', '0005_product_jp_candles'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='sold',
            field=models.TextField(default=''),
        ),
    ]
