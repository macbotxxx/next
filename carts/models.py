from django.db import models
from django.utils.translation import gettext_lazy as _

from store.models import Product, ProductVariation
from django.conf import settings
User = settings.AUTH_USER_MODEL

# Create your models here.


class Cart (models.Model):
    cart_id = models.CharField(max_length=400, blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class CartItem (models.Model):
    user = models.ForeignKey(
        User,
        verbose_name=_("User Profile"),
        on_delete=models.PROTECT, null=True,
        help_text=_("The user for whom account belongs to")
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_variation = models.ManyToManyField(ProductVariation,  blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)


    def sub_totals(self):
        return self.product.price * self.quantity

    def __unicode__(self):
        return self.product