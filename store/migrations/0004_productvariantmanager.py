# Generated by Django 3.1.13 on 2021-10-21 15:44

from django.db import migrations, models
import uuid

class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_productvariation'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductVariantManager',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, help_text='The unique identifier of an object.', primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]