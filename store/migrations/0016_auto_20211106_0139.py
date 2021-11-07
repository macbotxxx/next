# Generated by Django 3.1.13 on 2021-11-06 01:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0015_auto_20211106_0118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(help_text='Product image for the current product, which should be with no logo or trademark', null=True, upload_to='photos/products', verbose_name='Product Image'),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.ImageField(help_text='Product image for the current product, which should be with no logo or trademark', null=True, upload_to='photos/products', verbose_name='Product Image'),
        ),
    ]
