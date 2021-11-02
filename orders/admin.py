from django.contrib import admin
from .models import OrderProduct, Order, Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'payment_ref', 'payment_method', 'amount_paid', 'verified')
    list_display_link = ('user',)
    readonly_fields = ('payment_ref','amount_paid','payment_method','verified','status',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'payment', 'order_number', 'ip_address','is_ordered')
    list_display_link = ('user',)

@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('user', 'order', 'payment', 'ordered')
    list_display_link = ('user',)
