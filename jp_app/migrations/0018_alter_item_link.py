# Generated by Django 4.0.2 on 2022-07-29 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jp_app', '0017_alter_idea_production_costs_alter_idea_selling_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='link',
            field=models.URLField(blank=True, default=None, null=True),
        ),
    ]
