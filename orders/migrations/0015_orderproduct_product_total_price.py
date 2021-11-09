# Generated by Django 3.1.13 on 2021-11-07 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0014_auto_20211102_2343'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderproduct',
            name='product_total_price',
            field=models.IntegerField(blank=True, help_text='total price for the current product which is calculated by the quantity of the product with the product price.', null=True, verbose_name='Product Total Price '),
        ),
    ]