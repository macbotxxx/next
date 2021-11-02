from django.urls import path
from . import views

urlpatterns = [
    path ('place_order/', views.placeOrder, name='place_order'),
    path('verify-payment/<str:payment_ref>/', views.verify_payment, name='verify_payment'),
]