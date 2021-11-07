from django.urls import path
from . import views

urlpatterns = [
    path ('', views.user_index , name ="user_dashboard"),
    path ('order-review/<str:product_id>/', views.order_invoice , name ="get_product_id"),
    path('generate/pdf/', views.InvoicePDFView.as_view(), name='generate_pdf'),

]