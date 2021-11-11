from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View, ListView
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from carts.views import _cart_id
from carts.models import Cart, CartItem
from .forms import ReviewRatingForm
from orders.forms import OrderForm


from store.models import Product, ProductImage, ReviewRating
from categories.models import Category
from orders.models import OrderProduct



class HomePage(View):
    """ class base view for the homepage """

    def get (self, request, *args, **kwargs):
        products = Product.objects.all().filter(is_available = True, best_selling = True).order_by('-created_date')[:20]
        flash_sale = Product.objects.all().filter(flash_sale = True, is_available = True)[:20]
        onekitems = Product.objects.all().filter(is_available = True).order_by('price')[0:20]
        recommendedP = Product.objects.all().filter(is_available = True).order_by('-created_date')[:20]
    
        # getting the product rating
        reviews = [] 
        for product in products:
            reviews = ReviewRating.objects.filter(product_id=product.id)
                   

        context = {
            'products': products,
            'flash_sale':flash_sale,
            'reviews': reviews,
            'onekitems': onekitems,
            'recommendedP':recommendedP,
        }

        return render(self.request, 'pages/index.html', context)

    def post (self, request, *args, **kwargs):
        pass 



class ProductCategory (View):
    """ product category """

    def get (self, request, *args, **kwargs):

        category = Category.objects.get(slug= kwargs['slug'])
        if category.parent is None:
            products = Product.objects.filter(category__parent=category)
            count = products.count()

        else:
            products = Product.objects.filter(category=category)
            count = products.count()


    
        """product pagination"""
        paginator = Paginator(products, 20) # Show 20 contacts per page.
        page_number = request.GET.get('page')
        products = paginator.get_page(page_number)

        #  getting the product rating 
        for product in products:
            reviews = ReviewRating.objects.filter(product_id=product.id)

     
        context = {
            'category':category,
            'products': products,
            'reviews':reviews,
            'count':count,
        }

        return render(self.request, 'pages/category.html', context)

    def post (self, request, *args, **kwargs):
        pass



class ProductDetails (View):

    def get (self, request, *args, **kwargs):
        product = Product.objects.get(slug = kwargs['slug'])
        in_cart = CartItem.objects.filter(cart__cart_id =_cart_id(request), product = product).exists()
        related = Product.objects.all().filter(category__parent = product.category)

        # checking if the user actually ordered for the product before commentiing
        if request.user.is_authenticated:
            try:
                orderproduct = OrderProduct.objects.filter(user=request.user, product_id = product.id).exists()
            except OrderProduct.DoesNotExist:
                orderproduct = None
        else:
            orderproduct = None
        # getting the review of the product
        reviews = ReviewRating.objects.filter(product_id=product.id)
        review_count = reviews.count()

        # getting product multiple images
        try:
            images = ProductImage.objects.filter(product_id=product.id)
        except ProductImage.DoesNotExist:
            images = None


        context = {
            'product': product,
            'in_cart':in_cart,
            'related':related,
            'orderproduct':orderproduct,
            'reviews':reviews,
            'review_count':review_count,
            'images':images,
        }
        return render(self.request, 'pages/product_details.html', context)

    def post (self, request, *args, **kwargs):
        pass


def search_result(request):
    """
    Product search function using ajax
    """

    if request.is_ajax():
        res = None
        product = request.POST.get('product')
        qs = Product.objects.filter(product_name__icontains=product)
        if len(qs) > 0 and len(product) > 0:
            data = []
            for pos in qs:
                item = {
                    'slug': pos.slug,
                    'product_name':pos.product_name,
                    'price': pos.price,
                    'image': str(pos.image.url),

                }
                data.append(item)
            res = data
        else:
            res = 'No Product found.......'
        return JsonResponse({'data': res})

    return JsonResponse({})



class FlashSale (View):

    def get (self, request, *args, **kwargs):
        product = Product.objects.filter(flash_sale = True)
        count = product.count()

        """product pagination"""
        paginator = Paginator(product, 20) # Show 20 contacts per page.
        page_number = request.GET.get('page')
        product = paginator.get_page(page_number)


        
        context = {
            'product': product,
            'count':count,
        }
        return render(self.request, 'pages/flash_sale.html', context)

    def post (self, request, *args, **kwargs):
        pass



class Onekitems (View):
    """
    Showing items that are below one thousand naira
    """
    def get (self, request, *args, **kwargs):
        product =  Product.objects.all().filter(is_available = True).order_by('price')

        """product pagination"""
        paginator = Paginator(product, 20) # Show 20 contacts per page.
        page_number = request.GET.get('page')
        product = paginator.get_page(page_number)
        
        context = {
            'product': product,
        }
        return render(self.request, 'pages/flash_sale.html', context)

    def post (self, request, *args, **kwargs):
        pass


class BestSelling (View):
    """
    Showing items that are below one thousand naira
    """

    def get (self, request, *args, **kwargs):
        product =  Product.objects.all().filter(is_available = True).order_by('-created_date')

        """product pagination"""
        paginator = Paginator(product, 20) # Show 20 contacts per page.
        page_number = request.GET.get('page')
        product = paginator.get_page(page_number)
        
        context = {
            'product': product,
        }
        return render(self.request, 'pages/flash_sale.html', context)

    def post (self, request, *args, **kwargs):
        pass


class Checkout (LoginRequiredMixin, View):

    def get (self, request, total=0, quantity=0,shipping_rate_per_quantity = 0,grandtotal = 0,  cart_items=None):
        try:
            form = OrderForm(initial={'first_name': request.user.first_name,'last_name': request.user.last_name,'phone_number':request.user.contact_number,'email':request.user.email})
            if request.user.is_authenticated:
                cart_items = CartItem.objects.filter(user=request.user, is_active=True)
            else:
                cart = Cart.objects.get(cart_id = _cart_id(request))
                cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            for cart_item in cart_items:
                total += (cart_item.product.price * cart_item.quantity)
                quantity += cart_item.quantity
            shipping_rate_per_quantity = ( 100 * quantity )
            grandtotal = total + shipping_rate_per_quantity
        except:
            pass
        
        context = {
        'total': total,
        'quantity':quantity,
        'cart_items': cart_items,
        'shipping_rate_per_quantity':shipping_rate_per_quantity,
        'grandtotal': grandtotal,
        'form':form,
        }
        return render(self.request, 'pages/checkout.html', context)

    def post (self, request, *args, **kwargs):
        pass


def order_successfull(request):
    return render(request, 'pages/successful.html')


def review (request, product_id ):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id = request.user.id, product__id = product_id)
            form = ReviewRatingForm(request.POST, instance=reviews)
            if form.is_valid():            
                form.save()
                messages.success(request, 'Product review have been updated.')
                return redirect(url)
            else:
                messages.success(request, 'Product review form needs to be submitted.')
                return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewRatingForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.review = form.cleaned_data['review']
                data.rating = form.cleaned_data['rating']
                data.subject = form.cleaned_data['subject']
                data.product_id = product_id
                data.user = request.user
                data.save()
                messages.success(request, 'Product review have been sumitted.')
                return redirect(url)
            else:
                messages.success(request, 'Product review form needs to be submitted.')
                return redirect(url)
        
    else:
        messages.success(request, 'Product review form needs to be submitted.')
        return redirect(url)

    

