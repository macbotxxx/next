from .models import Cart, CartItem
from .views import _cart_id


def counter(request):
    cart_count = 0
    if 'admin' in request.path:
        return {}
    
    else:
        try:
            cart = Cart.objects.filter(cart_id=_cart_id(request))
            cart_items = CartItem.objects.all().filter(cart=cart[:1])
            for cart_item in cart_items:
                cart_count += cart_item.quantity
        except cart.DoesNotExist:
            cart_count = 0

    return dict(cart_count=cart_count)


def all_cart_items(request, total= 0):
    cart_items = CartItem.objects.all()
    for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
    return dict(cart_items=cart_items, total=total)

