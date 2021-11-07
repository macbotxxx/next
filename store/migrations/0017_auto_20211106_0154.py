# Generated by Django 3.1.13 on 2021-11-06 01:54

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0016_auto_20211106_0139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=django_resized.forms.ResizedImageField(crop=None, force_format='JPEG', help_text='Product image for the current product, which should be with no logo or trademark', keep_meta=True, null=True, quality=75, size=[640, 640], upload_to='photos/products', verbose_name='Product Image'),
        ),
    ]
