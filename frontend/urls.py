from django.urls import path
from . import views

urlpatterns = [

    path('', views.HomePage.as_view(), name ="homepage" ),
    path('category/<str:slug>/', views.ProductCategory.as_view() , name='category-detail'),  
    path('product-details/<str:slug>/', views.ProductDetails.as_view() , name='product-details')

]
