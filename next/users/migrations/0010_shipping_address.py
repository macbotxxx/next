# Generated by Django 3.1.13 on 2021-11-17 12:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_userregisteredip_is_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shipping_Address',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, help_text='The unique identifier of an object.', primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, help_text='Timestamp when the record was created.', max_length=20, verbose_name='Created Date')),
                ('modified_date', models.DateTimeField(default=django.utils.timezone.now, help_text='Modified date when the record was created.', max_length=20, verbose_name='Modified Date')),
                ('first_name', models.CharField(help_text='Customer legal first name', max_length=150, null=True, verbose_name='Legal First Name')),
                ('last_name', models.CharField(help_text='Customer legal last name', max_length=150, null=True, verbose_name='Legal Last Name ')),
                ('phone_number', models.CharField(help_text='Customers Phone Number', max_length=150, null=True, verbose_name='Phone Number ')),
                ('email', models.EmailField(help_text='Customer email address for discount and notifications', max_length=150, null=True, verbose_name='Customers Email')),
                ('address_line_1', models.CharField(help_text='Customers address line 1 ', max_length=400, null=True, verbose_name='Address Line 1')),
                ('address_line_2', models.CharField(blank=True, help_text='Customers address line 2 ', max_length=400, null=True, verbose_name='Address Line 2')),
                ('state', models.CharField(help_text='State of which the order is been placed from or to be shipped to.', max_length=400, null=True, verbose_name='Customers State')),
                ('city', models.CharField(help_text='City of which the order is been placed from or to be shipped to.', max_length=400, null=True, verbose_name='Order City')),
                ('user', models.ForeignKey(help_text='The user for whom account belongs to', null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='User Profile')),
            ],
            options={
                'verbose_name': 'User Shipping Addresses',
                'verbose_name_plural': 'User Shipping Addresses',
                'ordering': ('-created_date',),
            },
        ),
    ]