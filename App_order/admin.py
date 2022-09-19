from django.contrib import admin
from App_order.models import Cart, Order, OrderForVendorModel

# Register your models here.
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderForVendorModel)

