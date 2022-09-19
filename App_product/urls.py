from django.urls import path
from App_product import views

app_name = 'App_product'

urlpatterns = [
    path('', views.home, name='home'),
    path('fruit-shop/', views.shop_view, name='fruit-shop'),
    path('single-fruit/<pk>/', views.fruit_details, name='single-fruit'),
    path('seller_view/', views.seller_view, name='seller-view'),
    path('new-fruit/', views.new_fruit, name='new-fruit'),
    path('seller-order-view/', views.seller_order_view, name='seller-order-view'),
    path('seller-order-update-status/<pk>', views.seller_update_order_status, name='seller-order-update-status'),
]

