from django.db import models
from helpers.common.basemodel import BaseModel
from PIL import Image
from io import BytesIO
from django.utils.translation import gettext_lazy as _

class Wallpaper(BaseModel):
    desktop_image = models.ImageField(
        verbose_name= _('DeskTop Wallpaper'),
        max_length=255, null=True,
        help_text=_("a wallpaper is needed to be uploaded , and it the main bannner wallpaper.. note ... keep in mind the size of the image becuase it needs to be saved before image compressing by the app .")
    )

    mobile_image = models.ImageField(
        verbose_name= _('Mobile Wallpaper'),
        max_length=255, null=True,
        help_text=_("a wallpaper is needed to be uploaded , and it the main bannner wallpaper.. note ... keep in mind the size of the image becuase it needs to be saved before image compressing by the app .")
    )

    content = models.CharField(
        verbose_name= _('Content'),
       max_length = 500, null=True,
       help_text=_("content that will be dsiplayed on the banner image")
    )

    redirect_url = models.URLField(
        verbose_name= _('Redirect URL'),
        null=True, blank=True,
        help_text=_("this specify the redirect url of the banner image")
    )

    status  = models.BooleanField(
        verbose_name= _('Status'),
        default=False,null=True,
        help_text=_("the status of the current banner, which determain if the it should be active or not.")
    )

    def __str__(self):
        return str(self.desktop_image)

    #  to resize an image to a given height and width,
    def save(self, *args, **kwargs):
        if self.desktop_image:
            super().save(*args, **kwargs)
            # Image.open() can also open other image types
            img = Image.open(self.desktop_image.path)
            # WIDTH and HEIGHT are integers
            resized_img = img.resize((640, 640))
            resized_img.save(self.desktop_image.path)

        if self.mobile_image:
            super().save(*args, **kwargs)
            # Image.open() can also open other image types
            img = Image.open(self.mobile_image.path)
            # WIDTH and HEIGHT are integers
            resized_img = img.resize((640, 640))
            resized_img.save(self.mobile_image.path)

    class Meta:
        ordering = ('-created_date',)
        verbose_name = _("Banner Image")
        verbose_name_plural = _("Banner Image")


class FirstLayerImage (BaseModel):
    image = models.ImageField(
        verbose_name= _('Ad Image'),
        max_length=255, null=True,
        help_text=_("a wallpaper is needed to be uploaded , and it the main bannner wallpaper.. note ... keep in mind the size of the image becuase it needs to be saved before image compressing by the app .")
    )

    redirect_url = models.URLField(
        verbose_name= _('Redirect URL'),
        null=True, blank=True,
        help_text=_("this specify the redirect url of the banner image")
    )

    status  = models.BooleanField(
        verbose_name= _('Status'),
        default=False,null=True,
        help_text=_("the status of the current banner, which determain if the it should be active or not.")
    )

    def __str__(self):
        return str(self.image)

    #  to resize an image to a given height and width,
    def save(self, *args, **kwargs):
        if self.image:
            super().save(*args, **kwargs)
            # Image.open() can also open other image types
            img = Image.open(self.image.path)
            # WIDTH and HEIGHT are integers
            resized_img = img.resize((285, 229))
            resized_img.save(self.image.path)

    class Meta:
        ordering = ('-created_date',)
        verbose_name = _("First Layer Ad Image")
        verbose_name_plural = _("First Layer Ad Image")


class DownlayerImage (BaseModel):
    image = models.ImageField(
        verbose_name= _('Ad Image'),
        max_length=255, null=True,
        help_text=_("a wallpaper is needed to be uploaded , and it the main bannner wallpaper.. note ... keep in mind the size of the image becuase it needs to be saved before image compressing by the app .")
    )

    redirect_url = models.URLField(
        verbose_name= _('Redirect URL'),
        null=True, blank=True,
        help_text=_("this specify the redirect url of the banner image")
    )

    status  = models.BooleanField(
        verbose_name= _('Status'),
        default=False,null=True,
        help_text=_("the status of the current banner, which determain if the it should be active or not.")
    )

    def __str__(self):
        return str(self.image)

    #  to resize an image to a given height and width,
    def save(self, *args, **kwargs):
        if self.image:
            super().save(*args, **kwargs)
            # Image.open() can also open other image types
            img = Image.open(self.image.path)
            # WIDTH and HEIGHT are integers
            resized_img = img.resize((540, 270))
            resized_img.save(self.image.path)

    class Meta:
        ordering = ('-created_date',)
        verbose_name = _("Down Layer Image")
        verbose_name_plural = _("Down Layer Image")
