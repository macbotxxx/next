from django.shortcuts import get_object_or_404, render
from django.views.generic import View, ListView
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin

from carts.views import _cart_id
from carts.models import Cart, CartItem
from orders.forms import OrderForm


from store.models import Product
from categories.models import Category



class HomePage(View):
    """ class base view for the homepage """

    def get (self, request, *args, **kwargs):
        products = Product.objects.all().filter(is_available = True)
        flash_sale = Product.objects.all().filter(flash_sale = True)
        categories = Category.objects.all()
        for c in categories:
            print(c.parent)
           

        context = {
            'products': products,
            'categories': categories,
            'flash_sale':flash_sale,
        }

        return render(self.request, 'pages/index.html', context)

    def post (self, request, *args, **kwargs):
        pass 



class ProductCategory (View):
    """ product category """

    def get (self, request, *args, **kwargs):
        
        category = Category.objects.get(slug= kwargs['slug'])
        products = Product.objects.filter(category__parent=category)
    
        """product pagination"""
        paginator = Paginator(products, 20) # Show 20 contacts per page.
        page_number = request.GET.get('page')
        products = paginator.get_page(page_number)

        context = {
            'category':category,
            'products': products,
        }

        return render(self.request, 'pages/category.html', context)

    def post (self, request, *args, **kwargs):
        pass



class ProductDetails (View):

    def get (self, request, *args, **kwargs):
        product = Product.objects.get(slug = kwargs['slug'])
        in_cart = CartItem.objects.filter(cart__cart_id =_cart_id(request), product = product).exists()
        related = Product.objects.all().filter(category__parent = product.category)
        
        context = {
            'product': product,
            'in_cart':in_cart,
            'related':related,
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
        'form':form,
        }
        return render(self.request, 'pages/checkout.html', context)

    def post (self, request, *args, **kwargs):
        pass




# class ItemsByCategoryView(View):
    # ordering = 'id'
    # paginate_by = 10
    # template_name = 'pages/catpro.html'

    # def get(self, request, *args, **kwargs):
    #     # https://docs.djangoproject.com/en/3.1/topics/class-based-views/generic-display/#dynamic-filtering
    #     # the following category will also be added to the context data
    #     self.category = Category.objects.get(slug=self.kwargs['slug'])
    #     print(self.category)

    #     pass
    #     queryset = Product.objects.filter(category=self.category)
    #      # need to set ordering to get consistent pagination results
    #     queryset = queryset.order_by(self.ordering)
    #     return queryset

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['category'] = self.category
    #     return context

def getcat (request, slug = None ):


    categories = catoff.objects.get(slug=slug)
    queryset = Product.objects.filter(category__parent=categories)
    context = {
        'categories':categories,
        'queryset': queryset,
    }
    return render(request, 'pages/catpro.html', context)

