# Generated by Django 4.0.2 on 2022-08-09 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('to_do_list', '0003_alter_todolist_checked'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todolist',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
    ]