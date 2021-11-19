from django.core.checks import messages
from django.shortcuts import get_object_or_404, redirect, render

from carts.models import Cart, CartItem
from next.users.models import Shipping_Address
from store.models import Product
from .models import Order, OrderProduct, Payment
from .forms import OrderForm
from .payment_gateway import FlutterWave, PayStack
from django.contrib import messages

# Create your views here.

import random
import string

# django email settings
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# Generating random number...
def order_number():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

def transaction_ref():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=35))

def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid

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
    shipping_rate_per_quantity = ( 100 * quantity )
    grandtotal = total + shipping_rate_per_quantity

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():        
            use_default_shipping = form.cleaned_data.get(
                'use_default_shipping')
            if use_default_shipping:
                print("Using the defualt shipping address")
                address_qs = Shipping_Address.objects.filter(
                    user=request.user,
                    default=True,
                )

                if address_qs.exists():
                    shipping_address = address_qs[0]
                    data = Order()
                    data.shipping_address = shipping_address
                    data.user = current_user
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
                else:
                    pass

            else:
                first_name = form.cleaned_data['first_name'] 
                last_name = form.cleaned_data.get('last_name') 
                phone_number = form.cleaned_data.get('phone_number')
                email = form.cleaned_data.get('email')
                address_line_1 = form.cleaned_data.get('address_line_1')
                address_line_2 = form.cleaned_data.get('address_line_2') 
                state = form.cleaned_data.get('shipping_state')
                city = form.cleaned_data.get('shipping_local_gov')
                
                # changing the defualt shipping address 
                set_default_shipping = form.cleaned_data.get('set_default_shipping')
                if set_default_shipping:
                    address_qs = Shipping_Address.objects.filter(user=request.user,default=True,)
                    if address_qs.exists():
                        address_qs = Shipping_Address.objects.filter(user=request.user,default=True,).update(default=False)
                        save_default = form.cleaned_data.get('set_default_shipping')
                    else:
                        save_default = form.cleaned_data.get('set_default_shipping')
                        
                if  is_valid_form([first_name, last_name, phone_number, email, address_line_1, state,city]):
                   
                    # storing all the billing and order information in the order table 
                    # get and store the instance of the order information
                    data = Order()
                    data.user = current_user
                    address = Shipping_Address.objects.create(user = request.user, first_name = first_name, last_name = last_name, phone_number = phone_number, email = email, address_line_1 = address_line_1, address_line_2 = address_line_2, state = state , city = city, default = save_default)

                    data.shipping_address = address
                
                    data.shipping_rate_per_quantity = shipping_rate_per_quantity
                    data.order_total = grandtotal
                    data.ip_address = request.META.get('REMOTE_ADDR')
                    data.order_number = order_number()
                    data.save()
                    current_order = Order.objects.get(order_number = data.order_number, user = current_user, is_ordered = False)
                    
                    # saving user shipping adsress
                    


                    # creating payment
                    payment_ref = transaction_ref() 
                    payment = Payment.objects.create(user = current_user, payment_ref = payment_ref, amount_paid = grandtotal )
                    current_order.payment = payment
                    current_order.save()
            
                else:
                    messages.error(request, "Please fill in the required shipping address fields", extra_tags="warning")
                    return redirect('checkout')
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
            orderproduct.product_total_price = item.quantity * item.product.price
            orderproduct.ordered = True
            orderproduct.save()

            # adding the product variation to ordered table 
            print(item.product_id)
            cart_item = CartItem.objects.get(id=item.id)
            product_v = cart_item.product_variation.all()
            orderproduct = OrderProduct.objects.get(id = orderproduct.id)
            orderproduct.variation.set(product_v)
            orderproduct.save()

            # reduce the quantity of the order item 
            product = Product.objects.get(id = item.product_id)
            product.stock -= item.quantity
            product.save()

            # cleariing the cart item of the user
            CartItem.objects.filter(id=item.id).delete()

            #  sending email to the customer alerting him of the succesful order 
            # subject = 'Successful Order - Next Cash and Carry Online Store'
            # html_message = render_to_string(
            #     'emails/text.html',
            #     {
            #      'user': request.user,
            #     } 
            # )
            # plain_message = strip_tags(html_message)
            # from_email = 'From <admin@nextonline.com>'
            # to = request.user.email
            # mail.send_mail(subject, plain_message, from_email, [to], html_message = html_message) 

        return redirect('order_successful')
            
    else:
        print('payment not verified')
        return redirect('place_order')
    # return redirect('place_order')




