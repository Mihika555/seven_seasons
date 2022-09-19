from django.db import models
from django.conf import settings

# Different App model
from App_product.models import FruitModel


# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    item = models.ForeignKey(FruitModel, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    purchased = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.quantity} x {self.item.name}'

    def get_total(self):
        total = float(self.item.price * self.quantity)
        return format(total, '0.2f')


status_choice = (
    ('Processing', 'Processing'),
    ('Confirmed', 'Confirmed'),
    ('Rejected', 'Rejected'),
    ('Completed', 'Completed'),
)


class Order(models.Model):
    order_item = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='order_item')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='order')
    ordered = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    payment_id = models.CharField(max_length=264, blank=True, null=True)
    order_id = models.CharField(max_length=264, blank=True, null=True)
    status = models.CharField(max_length=20, default="Processing", choices=status_choice)

    def get_totals(self):
        total = 0
        total += float(self.order_item.get_total())
        return total


class OrderForVendorModel(models.Model):
    order_item = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='order_item_vendor')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customer_for_vendor')
    confirmed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    payment_id = models.CharField(max_length=264, blank=True, null=True)
    order_id = models.CharField(max_length=264, blank=True, null=True)

    def get_totals(self):
        total = 0
        total += float(self.order_item.get_total())
        return total
