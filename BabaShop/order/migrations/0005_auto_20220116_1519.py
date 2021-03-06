# Generated by Django 3.2.10 on 2022-01-16 11:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_auto_20220111_2051'),
        ('order', '0004_auto_20220111_2051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='total_price',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_quantity',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterUniqueTogether(
            name='orderitem',
            unique_together={('product', 'order')},
        ),
    ]
