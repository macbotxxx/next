from django.contrib import admin
from .models import OrderProduct, Order, Payment
import admin_thumbnails

# @admin_thumbnails.thumbnail('product')
class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('product_total_price','payment','user', 'quantity','variation', 'product_price', 'product','created_date', 'modified_date', 'ordered')
    extra = 0
   
    

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'payment_ref', 'payment_method', 'amount_paid', 'verified')
    list_display_link = ('user',)
    readonly_fields = ('user','payment_ref','amount_paid','payment_method','verified','status',)
    list_filter = ('created_date','user', 'verified','status', )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'payment', 'order_number', 'ip_address','is_ordered')
    list_display_link = ('user',)
    readonly_fields = ('user', 'payment', 'order_number', 'shipping_address', 'shipping_rate_per_quantity', 'order_total', 'tax', 'status', 'ip_address', 'is_ordered', 'created_date', 'modified_date', )
    inlines = [OrderProductInline]
    list_filter = ('created_date','user' )

@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('user', 'order', 'payment', 'ordered')
    list_display_link = ('user',)
    list_filter = ('created_date','user','ordered' )

