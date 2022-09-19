from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from App_order.models import Cart, Order
from App_payment.forms import BillingForm
from App_payment.models import BillingAddress
from App_product.models import FruitModel
from App_login.models import SellerModel


# Create your views here.
@login_required
def add_to_cart(request):
    pk = request.POST.get('pk')
    quantity = int(request.POST.get('quantity'))
    fruit = FruitModel.objects.get(id=pk)
    try:
        cart_item = Cart.objects.get(user=request.user, item=fruit, purchased=False)
        cart_item.quantity += quantity
        cart_item.save()
    except:
        cart_item = Cart.objects.create(user=request.user, item=fruit, quantity=quantity, purchased=False)
        cart_item.save()
    return HttpResponseRedirect(reverse('App_product:home'))


def remove_cart(request, pk):
    cart = Cart.objects.get(id=pk)
    cart.delete()
    return "done"


@login_required
def cart_showcasing(request):
    try:
        IsSeller = SellerModel.objects.get(seller=request.user)
    except:
        IsSeller = None

    cart = Cart.objects.filter(user=request.user, purchased=False)
    if request.method == 'POST':
        pk = request.POST.get('cart_pk')
        remove_cart(request, pk)
    fruit_price = 0.0
    for i in cart:
        fruit_price += float(i.get_total())
    vendors = [x.item.vendor for x in cart]
    delivery_charge = len(set(vendors)) * 150

    content = {
        'carts': cart,
        'cart_item': cart.count(),
        'fruit_price': fruit_price,
        'delivery_charge': delivery_charge,
        'total_cost': fruit_price + delivery_charge,
        'IsSeller': IsSeller
    }
    return render(request, 'App_order/cart_showcasing.html', context=content)


@login_required
def update_cart_quantity(request):
    cart_item = Cart.objects.get(id=request.POST.get('cart_item'), purchased=False)
    cart_item.quantity = request.POST.get('quantity')
    cart_item.save()
    return HttpResponseRedirect(reverse('App_order:cart-showcasing'))

# def order_cart_items(request):
#     cart_items = Cart.objects.filter(user=request.user, purchased=False)
#     for i in cart_items:
#         order = Order()
