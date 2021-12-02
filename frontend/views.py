from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View, ListView
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from carts.views import _cart_id
from carts.models import Cart, CartItem
from .forms import ReviewRatingForm, OrderTrackForm
from .filters import ProductFilter
from orders.forms import OrderForm
from next.users.models import Shipping_Address


from store.models import Product, ProductImage, ReviewRating
from categories.models import Category
from orders.models import Order, OrderProduct






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
        filter = ProductFilter()
        if category.parent is None:
            products = Product.objects.filter(category__parent=category)

        else:
            products = Product.objects.filter(category=category)


        myFilter = ProductFilter(request.GET, queryset=products)
        products = myFilter.qs
        count = products.count()
        
        """product pagination"""
        paginator = Paginator(products, 20) # Show 20 contacts per page.
        page_number = request.GET.get('page')
        products = paginator.get_page(page_number)
        

        #  getting the product rating 
        reviews = [] 
        for product in products:
            reviews = ReviewRating.objects.filter(product_id=product.id)
            
        

     
        context = {
            'category':category,
            'products': products,
            'reviews':reviews,
            'count':count,
            'filter':filter,
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
        reviews = [] 
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
        
        shipping_address_qs = Shipping_Address.objects.filter(
                user=self.request.user,
                default=True
            )
        
        if shipping_address_qs.exists():
            context.update(
                {
                'default_shipping_address': shipping_address_qs[0]
                })
            
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


def about_us (request):
    """about us page"""
    return render(request, 'pages/about_us.html')


def contact_us (request):
    """contact us page"""
    return render(request, 'pages/contact_us.html')

def our_stores (request):
    """our page page"""
    return render(request, 'pages/our_stores.html')

def faq (request):
    """faq page"""
    return render(request, 'pages/faq.html')

def order_tracker (request):
    """faq page"""
    form = OrderTrackForm()
    context = {
        'form': form,
    }
    return render(request, 'pages/order_track.html', context)

def get_brand (request, **kwargs):
    try:
        product = Product.objects.filter(brand=kwargs['id'])
    except Product.DoesNotExist:
        product = []

    """product pagination"""
    paginator = Paginator(product, 20) # Show 20 contacts per page.
    page_number = request.GET.get('page')
    product = paginator.get_page(page_number)

    context = {
        'product': product,
    }
    return render(request, 'pages/flash_sale.html', context)


def track_details(request):
    form = OrderTrackForm()
    if request.method == 'POST':
        form = OrderTrackForm(request.POST)
        if form.is_valid():
            number = form.cleaned_data.get('tracking_number')
            order = Order.objects.filter(order_number = number)
            if order.exists():
                my_order = order
                my_items = OrderProduct.objects.filter(order__order_number = number)
            else:
                messages.success(request, 'the order tracking number is invalid or inputed wrongly. Kindly check your order confirmation email or login to your dashboard. Still facing issues ?? chat our 24/7 customer care.', extra_tags = 'warning')
                return redirect('order_tracker')
        else:
            print('Invalid form')

        context = {
            'my_order': my_order,
            'my_items':my_items,
        }
    
    return render(request, 'pages/tracker_details.html', context)


    