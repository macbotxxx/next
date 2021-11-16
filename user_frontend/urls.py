from django.urls import path
from . import views

urlpatterns = [
    path ('', views.user_index , name ="user_dashboard"),
    path ('order-review/<str:product_id>/', views.order_invoice , name ="get_product_id"),
    path('generate/pdf/<str:product_id>/', views.InvoicePDFView.as_view(), name='generate_pdf'),
    path('profile-edit/', views.profile_edit, name = "profile_edit"),
    path('password-change/', views.password_change, name = "password_change"),
    path('my-orders/', views.my_orders, name = "my_orders"),

]