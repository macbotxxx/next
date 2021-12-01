from django.urls import path
from . import views


urlpatterns = [

    path('', views.HomePage.as_view(), name ="homepage" ),
    path('category/<str:slug>/', views.ProductCategory.as_view() , name='category-detail'),  
    path('product-details/<str:slug>/', views.ProductDetails.as_view() , name='product-details'),
    path('flash-sale/', views.FlashSale.as_view() , name='flash_sale'),
    path('1k-items/', views.Onekitems.as_view() , name='onekitems'),
    path('best-selling-items/', views.BestSelling.as_view() , name='BestSelling'),
    path('checkout/', views.Checkout.as_view() , name='checkout'),
    path('order-successful/', views.order_successfull, name='order_successful'),
    path('review/<str:product_id>/', views.review, name='review'),

    path('search/', views.search_result, name='search'),
    path('about-us/', views.about_us, name='about_us'),
    path('contact-us/', views.contact_us, name='contact_us'),
    path('our-stores/', views.our_stores, name='our_stores'),
    path('faq/', views.faq, name='faq'),
    path('get-brand/<str:id>/', views.get_brand, name='get_brand'),
    path('order-tracker/', views.order_tracker, name='order_tracker'),
    

]
