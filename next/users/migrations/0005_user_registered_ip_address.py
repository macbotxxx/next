# Generated by Django 3.1.13 on 2021-10-26 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20211006_1323'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='registered_ip_address',
            field=models.GenericIPAddressField(help_text='user default IP address hold the original ip address after registration, which a notification email will be sent to the user when a new ip address is been login to the account, and this is done for security reasons.', null=True, verbose_name='User Default IP Address'),
        ),
    ]
