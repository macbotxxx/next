# Generated by Django 3.1.13 on 2021-10-27 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_remove_productvariation_variations_category2'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='best_selling',
            field=models.BooleanField(default=False, help_text='to identify which product is among the best selling for the month.', null=True, verbose_name='Best Selling'),
        ),
        migrations.AddField(
            model_name='product',
            name='flash_sale',
            field=models.BooleanField(default=False, help_text='to identify which product is among the flash sale for the month.', null=True, verbose_name='Flash Sale'),
        ),
    ]
