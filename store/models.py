import uuid
from django.db import models
from django.urls.base import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from config.utils import unique_slug_generator_category, unique_slug_generator
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone


from categories.models import Category
from helpers.common.basemodel import BaseModel
from next.users.models import User


# Create your models here.
class Product(BaseModel):
    """ Product model"""
    product_sku = models.CharField(
        verbose_name=_('Product SKU'),
        max_length=500,
        null=True,
        help_text=_('Product sku should be added which identify each product')
    )

    product_name = models.CharField(
        verbose_name=_('Product Name'),
        max_length=500,
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

    old_price = models.IntegerField (
        verbose_name = _('Product Old Price'),
        null =True, blank=True,
        help_text= _('Product old price for the current product')
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

    best_selling = models.BooleanField (
        verbose_name = _("Best Selling"),
        default = False, null =True,
        help_text = _("to identify which product is among the best selling for the month.")
    )

    flash_sale  = models.BooleanField (
        verbose_name = _("Flash Sale"),
        default = False, null =True,
        help_text = _("to identify which product is among the flash sale for the month.")
    )
    
    class Meta:
        ordering = ('-created_date',)
        verbose_name = _("Add Product")
        verbose_name_plural = _("Add Products")

    def __str__(self):
        return str(self.product_name)

    def get_absolute_url(self):
        return reverse('product-details', args=[str(self.slug)])

    # def save(self, *args, **kwargs):
    #     value = self.product_name
    #     if not self.slug:
    #         self.slug = slugify(value, allow_unicode=True)
    #     super().save(*args, **kwargs)

# product slug 
def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
pre_save.connect(slug_generator, sender=Product)



# product variation manager interface
class ProductVariationManager(models.Manager):
    # variation function for the color of the product
    def colors (self):
        return super(ProductVariationManager, self).filter(variations_category="Color", is_active = True)

    # variation fucntion for thr product size
    def sizes (self):
        return super(ProductVariationManager, self).filter(variations_category="Size", is_active = True)


# product variation category list
VARIATION_CATEGORIES_LIST = (
    ('Color', 'Color'),
    ('Size', 'Size'),
)


class ProductVariation(BaseModel):
    """
    Product variations models for the current product function.
    """
    # registering custom manager interface
    objects = ProductVariationManager()

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        null=True,
        verbose_name = _('Product Name'),
        help_text = _('Product name refering to the product already uplaoded and to be added some variatons.')
    )

    variations_category = models.CharField(
        verbose_name = _('Variations'),
        max_length = 255,
        null=True,
        choices=VARIATION_CATEGORIES_LIST,
        help_text = _("Select which variation category to the current product")
    )

    variation_value = models.CharField(
        verbose_name = _('Variation Value'),
        null =True,
        max_length = 250,
        help_text=_("the value to select for the variation product")
    )

    is_active = models.BooleanField(
        verbose_name=_("Variation Status"),
        default = True,
        null =True,
        help_text=_("Status to dectect if the product variation is active or not")
    )
    

    class Meta:
        ordering = ('-created_date',)
        verbose_name = _("Product Variation ")
        verbose_name_plural = _("Product Variation")

    def __str__(self):
        return str(self.variation_value)


class ReviewRating(BaseModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        null=True,
        verbose_name = _('Product Name'),
        help_text = _('Product which the rating will be published to.')
    )

    user = models.ForeignKey(
        User,
        verbose_name=_("User Profile"),
        on_delete=models.PROTECT, null=True,
        help_text=_("The user for whom account belongs to")
    )

    subject = models.CharField(
        verbose_name = _('Product Review Subject'),
        null =True,
        max_length = 250,
        help_text=_("product review subjects")
    )

    review = models.TextField(
        verbose_name = _('Product Review'),
        null =True,
        max_length = 500,
        help_text=_("customer review the customer item.")
    )

    rating = models.IntegerField(
        verbose_name = _('Product Rating'),
        null =True,
    )

    status = models.BooleanField(
        verbose_name=_("Status"),
        default = True,
        null =True,
        help_text=_("Status to dectect if the product review is active or not")
    )


    class Meta:
        ordering = ('-created_date',)
        verbose_name = _("Product Review ")
        verbose_name_plural = _("Product Review")

    def __str__(self):
        return str(self.user)
