from django.shortcuts import get_object_or_404, render
from django.views.generic import View, ListView
from django.core.paginator import Paginator
from django.http import JsonResponse

from carts.views import _cart_id
from carts.models import Cart, CartItem


from store.models import Product
from categories.models import Category

# Create your views here.

def allCat(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }



class HomePage(View):
    """ class base view for the homepage """

    def get (self, request, *args, **kwargs):
        products = Product.objects.all().filter(is_available = True)
        categories = Category.objects.all()
        for c in categories:
            print(c.parent)
           

        context = {
            'products': products,
            'categories': categories,
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
    paginate_by = 2

    def get (self, request, *args, **kwargs):
        product = Product.objects.get(slug = kwargs['slug'])
        in_cart = CartItem.objects.filter(cart__cart_id =_cart_id(request), product = product).exists()
        
        context = {
            'product': product,
            'in_cart':in_cart,
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
        print(product)
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

