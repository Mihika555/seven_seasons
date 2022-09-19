from django.urls import path
from App_payment import views

app_name = 'App_payment'

urlpatterns = [
    path('checkout-page/', views.checkout_page, name='checkout-page'),
    path('payment', views.payment, name='payment'),
    path('purchased-complete/', views.purchased_complete, name='purchased-complete'),
    path('complete-payment/<val_id>/<tran_id>/', views.complete_payment, name='complete-payment'),
]

