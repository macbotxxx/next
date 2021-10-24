from django.contrib import admin

# Register your models here.
from .models import Cart, CartItem

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id', 'date')
    list_display = ('cart_id', 'date')


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product',  'cart', 'quantity', 'is_active')
    list_display_links = ('product',  'cart', 'quantity', 'is_active')