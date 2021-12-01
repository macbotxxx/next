# Generated by Django 3.1.13 on 2021-12-01 12:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0021_brands'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='brands',
            options={'ordering': ('-created_date',), 'verbose_name': 'Product Brand', 'verbose_name_plural': 'Product Brand'},
        ),
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(help_text='Product brand  will refrence the product brand table list, in any case the brand of the product is popular , the product can uplaod a new brand by clicking on the add brand button so to refrence the product to the brand. ', null=True, on_delete=django.db.models.deletion.CASCADE, to='store.brands', verbose_name='Product Brand'),
        ),
    ]
