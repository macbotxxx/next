# Generated by Django 3.1.13 on 2021-10-26 23:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_user_registered_ip_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserRegisteredIp',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, help_text='The unique identifier of an object.', primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, help_text='Timestamp when the record was created.', max_length=20, verbose_name='Created Date')),
                ('modified_date', models.DateTimeField(default=django.utils.timezone.now, help_text='Modified date when the record was created.', max_length=20, verbose_name='Modified Date')),
                ('registered_ip_address', models.GenericIPAddressField(help_text='user default IP address hold the original ip address after registration, which a notification email will be sent to the user when a new ip address is been login to the account, and this is done for security reasons.', null=True, verbose_name='User Default IP Address')),
                ('user', models.ForeignKey(help_text='The user for whom ip address belongs to', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='User Profile')),
            ],
            options={
                'verbose_name': 'User Registered IP Address',
                'verbose_name_plural': 'User Registered IP Address',
                'ordering': ('-created_date',),
            },
        ),
    ]