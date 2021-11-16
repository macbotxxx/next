import io
import tempfile

from codecs import decode
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.http import FileResponse
from django.views.generic import View, ListView
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from reportlab.pdfgen import canvas
from wkhtmltopdf.views import PDFTemplateView
from weasyprint import HTML

from .forms import ProfileSettingsForm
from orders.models import Order, OrderProduct
from store.models import Product, ProductImage, ReviewRating
from next.users.models import User


# Create your views here.
@login_required()
def user_index (request):
    order = Order.objects.all().filter(user=request.user, is_ordered = True).order_by('-created_date')[:10]
    context = {
        'order': order,
    }
    return render( request, 'user_dashboard/index.html', context)

@login_required()
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

@login_required()
def profile_edit (request):
    password = PasswordChangeForm(request.user)
    setting = ProfileSettingsForm(initial={'first_name': request.user.first_name,'last_name': request.user.last_name,'phone_number':request.user.contact_number})
    url = request.META.get('HTTP_REFERER')

    if request.method == 'POST':
        setting = ProfileSettingsForm(request.POST)
        if setting.is_valid():
            user_profile = User.objects.get(id=request.user.id)
            user_profile.first_name = setting.cleaned_data['first_name']
            user_profile.last_name = setting.cleaned_data['last_name']
            user_profile.phone_number = setting.cleaned_data['phone_number']
            user_profile.name = setting.cleaned_data['first_name'] + " " + setting.cleaned_data['last_name']
            user_profile.save()
            return redirect(url)

    context = {
        'password_form':password,
        'setting': setting,
    }
    return render(request,'user_dashboard/edit_profile.html', context)


@login_required()   
def password_change (request):
    if request.method == 'POST':
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # Important!
                messages.error(request, 'Your password was successfully updated!')


@login_required()
def my_orders (request):
    order = Order.objects.all().filter(user=request.user, is_ordered = True).order_by('-created_date')[:10]
    """product pagination"""
    paginator = Paginator(order, 20) # Show 20 contacts per page.
    page_number = request.GET.get('page')
    order = paginator.get_page(page_number)
    context = {
        'order': order,
    }
    return render( request, 'user_dashboard/my_orders.html', context)