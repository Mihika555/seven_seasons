import random

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect

# Import ListView
from django.views.generic import ListView, DetailView

# Login Required Mixin
from django.contrib.auth.mixins import LoginRequiredMixin

# Models
import App_product.models
from App_login.models import SellerModel
from App_order.models import Cart, Order
from App_blog.models import NutritionBlogModel
from .forms import FruitForm
from .models import FruitModel


# Create your views here.
def home(request):
    products = FruitModel.objects.filter(availability=True)
    products = products.order_by('-created_date')
    blogs = NutritionBlogModel.objects.all()
    first_six_blogs = blogs.order_by("-created_date")[:3]
    try:
        IsSeller = SellerModel.objects.get(seller=request.user)
    except:
        IsSeller = None

    if request.user.is_authenticated:
        cart_item = Cart.objects.filter(user=request.user, purchased=False).count()
    else:
        cart_item = 0
    first_three = products[:6]
    content = {
        'cart_item': cart_item,
        'IsSeller': IsSeller,
        'products': products,
        'first_three_products': first_three,
        'first_six_blogs': first_six_blogs
    }
    try:
        random_eight = random.choices(products, k=8)
        random_eight_ids = [x.id for x in random_eight]
        for i in range(len(random_eight_ids)):
            if random_eight_ids[i] % 2 == 0:
                random_eight_ids[i] = 2
            elif random_eight_ids[i] % 2 == 1:
                random_eight_ids[i] = 1
        content['random_eight'] = zip(random_eight, random_eight_ids)
    except:
        random_eight = 0
        random_eight_ids = 0
    return render(request, 'App_product/home.html', context=content)


def shop_view(request):
    try:
        IsSeller = SellerModel.objects.get(seller=request.user)
    except:
        IsSeller = None
    try:
        cart = Cart.objects.filter(user=request.user, purchased=False).count()
    except:
        cart = 0
    fruits = FruitModel.objects.all()
    content = {
        'fruits': fruits,
        'IsSeller': IsSeller,
        'cart_item': cart,
    }
    return render(request, 'App_product/shop-view.html', context=content)


def fruit_details(request, pk):
    try:
        IsSeller = SellerModel.objects.get(seller=request.user)
    except:
        IsSeller = None

    fruit = FruitModel.objects.get(id=pk)
    if request.user.is_authenticated:
        cart_item = Cart.objects.filter(user=request.user, purchased=False).count()
    else:
        cart_item = 0
    content = {
        'fruit': fruit,
        'cart_item': cart_item,
        'IsSeller': IsSeller,
    }
    return render(request, 'App_product/fruit_details.html', context=content)


@login_required
def seller_view(request):
    my_orders = Order.objects.filter(order_item__item__vendor=request.user)
    completed_order = Order.objects.filter(order_item__item__vendor=request.user, status='Completed')
    rejected_order = Order.objects.filter(order_item__item__vendor=request.user, status='Rejected')
    my_fruits = FruitModel.objects.filter(vendor=request.user)
    shop_name = SellerModel.objects.get(seller=request.user).shop_name
    content = {
        'my_fruits': my_fruits,
        'my_orders': my_orders,
        'shop_name': shop_name,
        'completed_order': completed_order,
        'canceled_order': rejected_order
    }
    return render(request, 'sellers/seller.html', context=content)


@login_required
def new_fruit(request):
    my_fruits = FruitModel.objects.filter(vendor=request.user)
    form = FruitForm()
    if request.method == 'POST':
        form = FruitForm(request.POST, request.FILES)
        if form.is_valid():
            this_form = form.save(commit=False)
            this_form.vendor = request.user
            this_form.save()
            return HttpResponseRedirect(reverse('App_product:seller-view'))

    shop_name = SellerModel.objects.get(seller=request.user).shop_name
    content = {
        'form': form,
        'shop_name': shop_name,
        'my_fruits': my_fruits,
    }
    return render(request, 'sellers/new_fruit.html', context=content)


@login_required
def seller_order_view(request):
    my_orders = Order.objects.filter(order_item__item__vendor=request.user).order_by('-created')
    shop_name = SellerModel.objects.get(seller=request.user).shop_name
    content = {
        'my_orders': my_orders,
        'shop_name': shop_name,
    }
    return render(request, 'App_product/seller_order-view.html', context=content)


def seller_update_order_status(request, pk):
    my_order = Order.objects.get(id=pk)
    print(my_order)
    if request.method == 'GET':
        new_status = request.GET.get('status')
        print(new_status)
        my_order.status = new_status
        my_order.save()
        return HttpResponseRedirect(reverse('App_product:seller-order-view'))

