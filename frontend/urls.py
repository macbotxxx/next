from django.urls import path
from . import views

urlpatterns = [

    path('', views.HomePage.as_view(), name ="homepage" ),
    path('category/<str:slug>/', views.ProductCategory.as_view() , name='category-detail'),  
    path('product-details/<str:slug>/', views.ProductDetails.as_view() , name='product-details'),
    path('flash-sale', views.FlashSale.as_view() , name='flash_sale'),
    path('checkout', views.Checkout.as_view() , name='checkout'),

    path('search/', views.search_result, name='search'),

]
