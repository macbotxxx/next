from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add-to-cart/<str:id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<str:id>/', views.remove_from_cart, name='remove_from_cart'),
    path('delete-cart/<str:id>/', views.delete_cart, name='delete_cart'),
]
