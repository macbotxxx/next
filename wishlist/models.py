from django.db import models
from django.utils.translation import gettext_lazy as _
from helpers.common.basemodel import BaseModel

from store.models import Product
from django.conf import settings
User = settings.AUTH_USER_MODEL

# Create your models here.


class Wishlist (BaseModel):
    user = models.ForeignKey(
        User,
        verbose_name=_("User Profile"),
        on_delete=models.PROTECT, null=True,
        help_text=_("The user for whom account belongs to")
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        null=True,
        verbose_name = _("Product"),
        help_text = _("The product that is added to wishlist by the user")
        )

    def __str__(self):
        return str(self.user)

    class Meta:
        ordering = ('-created_date',)
        verbose_name = _("My Wishlist")
        verbose_name_plural = _("My Wishlist")