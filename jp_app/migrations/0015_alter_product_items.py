# Generated by Django 4.0.2 on 2022-07-24 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jp_app', '0014_alter_product_items'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='items',
            field=models.ManyToManyField(blank=True, default=[], related_name='productsit', to='jp_app.Item'),
        ),
    ]
