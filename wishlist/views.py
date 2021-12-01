from django.shortcuts import get_object_or_404, redirect, render
from store.models import Product, ProductVariation
from .models import Wishlist

# Create your views here.

from django.http import HttpResponse
import random
import string

def add_to_wishlist(request, **kwargs):
    url = request.META.get('HTTP_REFERER')
    try:
        product = Product.objects.get(pk=kwargs['product_id'])
    except Product.DoesNotExist:
        return redirect(url)
    products = Wishlist.objects.filter(user=request.user, product=product)
    if products.exists():
        return redirect(my_wishlist)
    else:
        Wishlist.objects.create(user=request.user, product=product)
        return redirect(my_wishlist)


def my_wishlist(request):
    try:
        my_wish = Wishlist.objects.filter(user=request.user)
    except Wishlist.DoesNotExist:
        my_wish = 0

    context = {
        'my_wish': my_wish,
    }
    return render(request, 'pages/wishlist.html', context )


def delete_wishlist(request, **kwargs):
    Wishlist.objects.filter(user=request.user, pk=kwargs['id']).delete()
    return redirect(my_wishlist)



    


