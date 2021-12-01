# Generated by Django 3.1.13 on 2021-12-01 12:46

from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0020_product_short_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brands',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, help_text='The unique identifier of an object.', primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, help_text='Timestamp when the record was created.', max_length=20, verbose_name='Created Date')),
                ('modified_date', models.DateTimeField(default=django.utils.timezone.now, help_text='Modified date when the record was created.', max_length=20, verbose_name='Modified Date')),
                ('brand', models.CharField(help_text='This holds the brand name.', max_length=500, null=True, verbose_name='Brand')),
                ('brand_image', models.ImageField(help_text='uplaod the brand image , which should be PNG , JPEG, JPG', null=True, upload_to='brands/', verbose_name='Brand Image')),
            ],
            options={
                'verbose_name': 'Brands',
                'verbose_name_plural': 'Brand',
                'ordering': ('-created_date',),
            },
        ),
    ]
