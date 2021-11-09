from codecs import decode
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.template.loader import render_to_string

from orders.models import Order, OrderProduct
from store.models import Product, ProductImage, ReviewRating


from weasyprint import HTML
import tempfile

import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from wkhtmltopdf.views import PDFTemplateView



# Create your views here.

def user_index (request):
    order = Order.objects.all().filter(user=request.user, is_ordered = True).order_by('-created_date')[:10]
    context = {
        'order': order,
    }
    return render( request, 'user_dashboard/index.html', context)


def order_invoice (request, product_id):
    order = OrderProduct.objects.get(id = product_id)
    context = {
        'order': order,
    }
    return render( request, 'user_dashboard/index.html', context)



class InvoicePDFView(PDFTemplateView):
    template_name = "invoice/pdf.html"
    item_total = 0

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = OrderProduct.objects.filter(order__order_number = context['product_id'])[:1]
        order_item = OrderProduct.objects.filter(order__order_number = context['product_id'])
        for i in order_item:
            item_total = i.quantity * i.product.price 
            print(item_total)
        
        context['products'] = products
        context['order_item'] = order_item
        context['item_total'] = item_total
        return context

   