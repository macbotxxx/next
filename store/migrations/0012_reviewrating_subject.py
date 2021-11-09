# Generated by Django 3.1.13 on 2021-11-03 01:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_reviewrating'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewrating',
            name='subject',
            field=models.CharField(help_text='product review subjects', max_length=250, null=True, verbose_name='Product Review Subject'),
        ),
    ]