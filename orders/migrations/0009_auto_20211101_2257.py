# Generated by Django 3.1.13 on 2021-11-01 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_auto_20211101_2256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='amount_paid',
            field=models.IntegerField(help_text='Amount paid for the above order by the customer.', null=True, verbose_name='Amount Paid'),
        ),
    ]
