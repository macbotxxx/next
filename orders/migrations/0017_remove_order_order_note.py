# Generated by Django 3.1.13 on 2021-11-18 01:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0016_auto_20211118_0054'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='order_note',
        ),
    ]