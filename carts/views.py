from django.shortcuts import redirect, render
from store.models import Product
from .models import Cart, CartItem

# Create your views here.


def cart (request):
    return render(request, 'pages/cart.html')


def _cart_id (request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_to_cart (request, id):
    product = Product.objects.get(id=id) #get the product

    try: 
        cart = Cart.objects.get(cart_id = _cart_id(request))  #get the cart_id present in the session
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id = _cart_id(request))
    cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1 
    
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(product=product, quantity=1, cart = cart)
        cart_item.save()

    return redirect('cart')

