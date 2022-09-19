from django.urls import path
from App_admin import views

app_name = 'App_admin'

urlpatterns = [
    path('', views.admin_home, name='home'),
    path('all-stores/', views.admin_stores, name='all-stores'),
    path('verify-store/<int:pk>', views.verify_store, name='verify-store'),
    path('orders/', views.orders, name='orders'),
]
