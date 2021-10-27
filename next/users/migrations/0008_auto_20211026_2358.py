# Generated by Django 3.1.13 on 2021-10-26 23:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20211026_2353'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userregisteredip',
            options={'ordering': ('-created_date',), 'verbose_name': 'users Registered IP Address', 'verbose_name_plural': 'users Registered IP Address'},
        ),
        migrations.AddField(
            model_name='userregisteredip',
            name='registered_ip_address',
            field=models.GenericIPAddressField(help_text='user default IP address hold the original ip address after registration, which a notification email will be sent to the user when a new ip address is been login to the account, and this is done for security reasons.', null=True, verbose_name='User Default IP Address'),
        ),
        migrations.AddField(
            model_name='userregisteredip',
            name='user',
            field=models.ForeignKey(help_text='The user for whom account belongs to', null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='User Profile'),
        ),
    ]
