# Generated by Django 4.0.2 on 2022-07-29 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jp_app', '0018_alter_item_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='link',
            field=models.URLField(blank=True, default=0, null=True),
        ),
    ]
