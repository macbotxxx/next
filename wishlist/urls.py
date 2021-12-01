from django.urls import path
from . import views

urlpatterns = [
    path('my-wishlist/', views.my_wishlist, name ="my_wishlist"),
    path('add-to-list/<str:product_id>/', views.add_to_wishlist, name ="add_to_wishlist"),
    path('delete-from-list/<str:id>/', views.delete_wishlist, name ="delete_wishlist"),
]