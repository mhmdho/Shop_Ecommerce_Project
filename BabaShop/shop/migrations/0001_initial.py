# Generated by Django 3.2.10 on 2021-12-29 12:23

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('myuser', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ProductTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'pro_tag',
                'verbose_name_plural': 'pro_tags',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('name', models.CharField(max_length=50)),
                ('type', models.CharField(choices=[('SUPERMARKET', 'Supermarket'), ('HYPERMARKET', 'Hypermarket'), ('GREENGROCER', 'Greengrocer'), ('FRUIT STORE', 'fruit store'), ('ORGANIC STORE', 'Organic store'), ('CONVENIENCE STORE', 'Convenience store')], default='SUPERMARKET', max_length=17)),
                ('address', models.CharField(max_length=200)),
                ('supplier', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='myuser.customuser')),
                ('is_confirmed', models.BooleanField(default=False)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6, validators=[django.core.validators.MinValueValidator(0.01)])),
                ('stock', models.IntegerField(default=0)),
                ('weight', models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(0.01)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('description', models.TextField(max_length=400)),
                ('is_active', models.BooleanField(default=False)),
                ('is_confirmed', models.BooleanField(default=False)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.productcategory')),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.shop')),
                ('tag', models.ManyToManyField(blank=True, to='shop.ProductTag')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='product_image/')),
                ('default', models.BooleanField(default=False)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_img', to='shop.product')),
            ],
        ),
    ]