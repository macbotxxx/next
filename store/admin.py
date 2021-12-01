from django.contrib import admin
from .models import Product, ProductVariation, ReviewRating, ProductImage, Brands

import admin_thumbnails

@admin.register(Brands)
@admin_thumbnails.thumbnail('brand_image')
class BrandsAdmin(admin.ModelAdmin):
    list_display = ('brand', 'brand_image')
    list_display_links = ('brand', 'brand_image')

class ProductVariationTabular(admin.TabularInline):
    model = ProductVariation
    fields = ('variations_category','variation_value', 'is_active')
    extra = 1

@admin_thumbnails.thumbnail('image')
class ProductImageTabular(admin.TabularInline):
    model = ProductImage

# All product admin models 
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'is_available', 'category', 'modified_date')
    list_display_links = ('product_name', 'price', 'stock', 'is_available', 'category')
    inlines = [ProductVariationTabular, ProductImageTabular]

# product variation models 
@admin.register(ProductVariation)
class ProductVariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variations_category', 'variation_value', 'is_active')
    list_display_links = ('product', 'variations_category', 'variation_value')
    list_editable = ('is_active',)


@admin.register(ReviewRating)
class ReviewRatingAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'review', 'rating', 'status')
    list_display_links = ('user',)