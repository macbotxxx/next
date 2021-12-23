# Generated by Django 3.1.13 on 2021-12-23 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banners', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wallpaper',
            name='image',
        ),
        migrations.AddField(
            model_name='wallpaper',
            name='desktop_image',
            field=models.ImageField(help_text='a wallpaper is needed to be uploaded , and it the main bannner wallpaper.. note ... keep in mind the size of the image becuase it needs to be saved before image compressing by the app .', max_length=255, null=True, upload_to='', verbose_name='DeskTop Wallpaper'),
        ),
        migrations.AddField(
            model_name='wallpaper',
            name='mobile_image',
            field=models.ImageField(help_text='a wallpaper is needed to be uploaded , and it the main bannner wallpaper.. note ... keep in mind the size of the image becuase it needs to be saved before image compressing by the app .', max_length=255, null=True, upload_to='', verbose_name='Mobile Wallpaper'),
        ),
    ]
