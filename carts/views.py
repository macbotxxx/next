from django.shortcuts import get_object_or_404, redirect, render
from store.models import Product, ProductVariation
from .models import Cart, CartItem

# Create your views here.

from django.http import HttpResponse
import random
import string

def cart_number():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=45))


def _cart_id (request):
    cart = request.session.get('cart_x')
    if not cart:
        cart = request.session['cart_x'] = cart_number()
    return cart


def add_to_cart (request, id):
    product = Product.objects.get(id=id) #get the product
    variations = [] 
    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[key]
            try:
                variation = ProductVariation.objects.get(product = product , variation_value__iexact=value,  variations_category__iexact=key)
                variations.append(variation)
            except:
                pass

    try: 
        cart = Cart.objects.get(cart_id = _cart_id(request))  #get the cart_id present in the session
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id = _cart_id(request))
    cart.save()

    is_cart_item_exist = CartItem.objects.filter(product=product, cart= cart).exists() #checking if the product and variation exists
    if is_cart_item_exist:
        cart_item = CartItem.objects.filter(product=product, cart=cart) 

        ex_var_list = []
        id = []

        for item in cart_item:
            existing_variation = item.product_variation.all()
            ex_var_list.append(list(existing_variation))
            id.append(item.id)

        if variations in ex_var_list:
            # increase the cart quantity by one 
            index = ex_var_list.index(variations)
            item_id = id[index]
            item = CartItem.objects.get( product=product, id=item_id)
            item.quantity += 1
            item.save() 
            
        else:
            item = CartItem.objects.create(product=product, quantity=1, cart = cart)
            if len(variations) > 0:
                item.product_variation.clear()
                item.product_variation.add(*variations)
            item.save()
            
    else:
       
        cart_item = CartItem.objects.create(
            product=product, 
            quantity=1, 
            cart = cart
        )
        if len(variations) > 0 : #adding product to cart
            cart_item.product_variation.clear() # clearing the previous product variation
            cart_item.product_variation.add(*variations)
        cart_item.save() 
    return redirect('cart')


def remove_from_cart (request, id, c_id):
    print(c_id)
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=id)
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart, id = c_id )
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass

    return redirect('cart')

def delete_cart(request, id, c_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=id)
    cart_item = CartItem.objects.filter(product=product, cart=cart, id = c_id )
    cart_item.delete()
    return redirect('cart')



def cart (request, total=0, quantity=0, cart_items=None):

    try:
        cart = Cart.objects.get(cart_id = _cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        shipping_rate_per_quantity = ( 800 * quantity )
        grandtotal = total + shipping_rate_per_quantity
    except:
        pass

    context = {
        'total': total,
        'quantity':quantity,
        'cart_items': cart_items,
        'shipping_rate_per_quantity':shipping_rate_per_quantity,
        'grandtotal': grandtotal,
    }


    return render(request, 'pages/cart.html', context)


