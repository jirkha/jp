# Generated by Django 4.0.2 on 2022-07-31 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jp_app', '0021_remove_product_production_costs_alter_item_supplier'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='production_costs',
            field=models.IntegerField(default=0),
        ),
    ]
