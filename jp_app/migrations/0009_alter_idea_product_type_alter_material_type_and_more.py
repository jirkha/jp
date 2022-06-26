# Generated by Django 4.0.2 on 2022-06-26 17:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jp_app', '0008_remove_transaction_selling_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='idea',
            name='product_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_types_2', to='jp_app.producttype'),
        ),
        migrations.AlterField(
            model_name='material',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='types', to='jp_app.materialtype'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_types', to='jp_app.producttype'),
        ),
        migrations.AlterField(
            model_name='removal',
            name='material',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='removals', to='jp_app.material'),
        ),
        migrations.AlterField(
            model_name='removal',
            name='material_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='removal_types', to='jp_app.materialtype'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sale_types', to='jp_app.saletype'),
        ),
        migrations.AlterField(
            model_name='storage',
            name='material',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='materials', to='jp_app.material'),
        ),
        migrations.AlterField(
            model_name='storage',
            name='material_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='material_types', to='jp_app.materialtype'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='jp_app.product'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='sales_channel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales', to='jp_app.sale'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='total_price',
            field=models.FloatField(blank=True),
        ),
    ]
