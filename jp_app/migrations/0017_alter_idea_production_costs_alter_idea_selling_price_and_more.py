# Generated by Django 4.0.2 on 2022-07-29 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jp_app', '0016_item_link_item_supplier_product_procedure_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='idea',
            name='production_costs',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='idea',
            name='selling_price',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='material',
            name='price',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='material',
            name='quantity_of_material',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='product',
            name='sold',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='removal',
            name='quantity_of_material',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='storage',
            name='price',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='storage',
            name='quantity_of_material',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='total_price',
            field=models.IntegerField(blank=True),
        ),
    ]