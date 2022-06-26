# Generated by Django 4.0.2 on 2022-06-26 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jp_app', '0007_remove_product_selling_price_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='selling_price',
        ),
        migrations.AddField(
            model_name='transaction',
            name='product_price',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='transaction',
            name='total_price',
            field=models.FloatField(blank=True, default=0),
        ),
    ]