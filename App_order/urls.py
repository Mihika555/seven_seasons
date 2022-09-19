from django.urls import path
from App_order import views
app_name = 'App_order'

urlpatterns = [
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart-showcasing/', views.cart_showcasing, name='cart-showcasing'),
    path('update-cart-quantity/', views.update_cart_quantity, name='update-cart-quantity'),
]

