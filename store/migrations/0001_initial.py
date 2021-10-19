# Generated by Django 3.1.13 on 2021-10-08 10:08

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categories', '0002_auto_20211008_1008'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, help_text='The unique identifier of an object.', primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, help_text='Timestamp when the record was created.', max_length=20, verbose_name='Created Date')),
                ('modified_date', models.DateTimeField(default=django.utils.timezone.now, help_text='Modified date when the record was created.', max_length=20, verbose_name='Modified Date')),
                ('product_name', models.CharField(help_text='Product name should be added which identify each product', max_length=500, null=True, unique=True, verbose_name='Product Name')),
                ('slug', models.SlugField(blank=True, help_text='Slug field for the category which is auto generated when the product name is been created', max_length=300, null=True, verbose_name='Product Slug')),
                ('description', models.TextField(help_text='Product description for the current product and note it should be well organized and explainable.', null=True, verbose_name='Product Description')),
                ('price', models.IntegerField(help_text='Product price for the current product', null=True, verbose_name='Product Price')),
                ('image', models.ImageField(help_text='Product image for the current product, which should be with no logo or trademark', null=True, upload_to='photos/products', verbose_name='Product Image')),
                ('stock', models.IntegerField(help_text='Product availablity for the current item , which will automatically be tagged as out of stock when it reduces to zero.', null=True, verbose_name='Total Stock')),
                ('is_available', models.BooleanField(default=True, help_text='Product availablity for this is item is been activated to false when the stock is less than 1 or activated to true when the stcok is greater than one', null=True, verbose_name='Product availablity')),
                ('category', models.ForeignKey(help_text='Product category will refrence the product category table which when the category is been deleted the items related to the parent or child category will be deleted as well.', null=True, on_delete=django.db.models.deletion.CASCADE, to='categories.category', verbose_name='Product category')),
            ],
            options={
                'verbose_name': 'Add Product',
                'verbose_name_plural': 'Add Products',
                'ordering': ('-created_date',),
            },
        ),
    ]
