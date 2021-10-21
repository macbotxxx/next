from django.shortcuts import get_object_or_404, redirect, render
from store.models import Product
from .models import Cart, CartItem

# Create your views here.

from django.http import HttpResponse



def _cart_id (request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_to_cart (request, id):
    if request.method == 'POST':

        color = request.POST['color']
        # size = request.GET['size']

        return HttpResponse( color)
        exit()
    product = Product.objects.get(id=id) #get the product

    try: 
        cart = Cart.objects.get(cart_id = _cart_id(request))  #get the cart_id present in the session
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id = _cart_id(request))
    cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1  #increase the cart quantity + 1
        cart_item.save() 

    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product, 
            quantity=1, 
            cart = cart
        )
        cart_item.save() 
    return redirect('cart')


def remove_from_cart (request, id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()

    else:
        cart_item.delete()

    return redirect('cart')

def delete_cart(request, id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
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
