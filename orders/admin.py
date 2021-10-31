from django.contrib import admin
from .models import OrderProduct, Order, Payement

@admin.register(Payement)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'payment_id', 'payment_method', 'amount_paid', 'status')
    list_display_link = ('user',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'payment', 'order_number', 'ip_address','is_ordered')
    list_display_link = ('user',)

@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('user', 'order', 'payment', 'ordered')
    list_display_link = ('user',)
