from django.core.checks import messages
from django.shortcuts import get_object_or_404, redirect, render

from carts.models import Cart, CartItem
from store.models import Product
from .models import Order, OrderProduct, Payment
from .forms import OrderForm
from .payment_gateway import FlutterWave, PayStack

# Create your views here.

import random
import string

# Generating random number...
def order_number():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

def transaction_ref():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=35))


def placeOrder (request,total=0, quantity=0):
    current_user = request.user
    shipping_rate_per_quantity = 0
    grandtotal = 0

    # if the cart count is less than 1 , then redirect the customer to the store page

    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()

    if cart_count <= 0:
        return redirect('/')

    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    shipping_rate_per_quantity = ( 800 * quantity )
    grandtotal = total + shipping_rate_per_quantity

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # storing all the billing and order information in the order table 
            # get and store the instance of the order information
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone_number = form.cleaned_data['phone_number']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.shipping_rate_per_quantity = shipping_rate_per_quantity
            data.order_total = grandtotal
            data.ip_address = request.META.get('REMOTE_ADDR')
            data.order_number = order_number()
            data.save()
            current_order = Order.objects.get(order_number = data.order_number, user = current_user, is_ordered = False)


            # creating payment
            payment_ref = transaction_ref() 
            payment = Payment.objects.create(user = current_user, payment_ref = payment_ref, amount_paid = grandtotal )
            current_order.payment = payment
            current_order.save()
            

            context = {
                'current_order':current_order,
                'shipping_rate_per_quantity': shipping_rate_per_quantity,
                'grandtotal': grandtotal,
                'cart_items':cart_items,
                'payment_ref':payment_ref,
            }

            return render(request, 'pages/payment.html', context)
        
        else:
            return redirect('checkout')


# to verify payment before saving billing status
def verify_payment (request, payment_ref):
    # payment = Payment.objects.filter(payment_ref=payment_ref)
    payment = get_object_or_404(Payment, payment_ref=payment_ref)
    verified = payment.verify_payment()
    
    print('order is saved and updated')
    if verified:
        order = Order.objects.get(payment = payment, user = request.user)
        order.is_ordered = True
        order.save()
        payment.status = 'success'
        payment.save()
        print('payment verified')
        cart_items = CartItem.objects.filter(user = request.user)
        for item in cart_items:
            orderproduct = OrderProduct()
            orderproduct.order_id = order.id
            orderproduct.payment = payment
            orderproduct.user = request.user
            orderproduct.product_id = item.product_id
            orderproduct.quantity = item.quantity
            orderproduct.product_price = item.product.price
            orderproduct.ordered = True
            orderproduct.save()

            # adding the product variation to ordered table 
            cart_item = CartItem.objects.get(id = item.id)
            product_v = cart_item.product_variation.all()
            orderproduct = OrderProduct.objects.get(id = orderproduct.id)
            orderproduct.variation.set(product_v)
            orderproduct.save()

            # reduce the quantity of the order item 
            product = Product.objects.get(id = item.product_id)
            product.stock -= item.quantity
            product.save()

            # cleariing the cart item of the user
            CartItem.objects.filter(user = request.user).delete() 
            
    else:
        print('payment not verified')
    # return redirect('checkout')




