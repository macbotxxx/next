from django.db import models
from django.utils.translation import gettext_lazy as _
from config.utils import unique_slug_generator_category
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from next.categories.models import Category
from helpers.common.basemodel import BaseModel


# Create your models here.
class Product(BaseModel):
    """ Product model"""

    product_name = models.CharField(
        verbose_name=_('Product Name'),
        max_length=500,
        unique=True,
        null=True,
        help_text=_('Product name should be added which identify each product')
    )

    slug = models.SlugField(
        verbose_name = _('Product Slug'),
        null=True,
        max_length=300, blank=True,
        help_text= _('Slug field for the category which is auto generated when the product name is been created')
    )

    description = models.TextField(
        verbose_name = _('Product Description'),
        null=True,
        help_text= _('Product description for the current product and note it should be well organized and explainable.')
    )

    price = models.IntegerField (
        verbose_name = _('Product Price'),
        null =True,
        help_text= _('Product price for the current product')
    )

    image = models.ImageField(
        verbose_name = _('Product Image'),
        upload_to = "photos/products",
        null =True,
        help_text= _('Product image for the current product, which should be with no logo or trademark')
    )

    stock = models.IntegerField(
        verbose_name = _('Total Stock'),
        null=True,
        help_text= _('Product availablity for the current item , which will automatically be tagged as out of stock when it reduces to zero.')
    )

    is_available = models.BooleanField(
        verbose_name = _('Product availablity'),
        default=True,
        null=True,
        help_text= _('Product availablity for this is item is been activated to false when the stock is less than 1 or activated to true when the stcok is greater than one')
    )

    category = models.ForeignKey(
        Category, on_delete = models.CASCADE,
        verbose_name = _("Product category"),
        null =True,
        help_text= _('Product category will refrence the product category table which when the category is been deleted the items related to the parent or child category will be deleted as well.')

    )

    



def slug_generator_category(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator_category(instance)


pre_save.connect(slug_generator_category, sender=Product)