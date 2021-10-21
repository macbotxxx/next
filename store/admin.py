from django.contrib import admin
from .models import Product, ProductVariation

# All product admin models 
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'is_available', 'category', 'modified_date')
    list_display_links = ('product_name', 'price', 'stock', 'is_available', 'category')

# product variation models 
@admin.register(ProductVariation)
class ProductVariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variations_category', 'variation_value', 'is_active')
    list_display_links = ('product', 'variations_category', 'variation_value')
    list_editable = ('is_active',)