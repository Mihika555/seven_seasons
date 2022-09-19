import re
import uuid

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User

# Create your views here.
from django.urls import reverse

from App_login.forms import SignUpForm, ProfileForm, ContactUsForm, SellerForm
from App_login.models import Profile
from App_order.models import Order, Cart
from App_login.models import SellerModel


def signup_system(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('App_login:login'))
    content = {
        'form': form,
    }
    return render(request, 'App_login/signup_page.html', context=content)


def login_system(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user_email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=user_email, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse('App_product:home'))
    content = {
        'form': form,
    }
    return render(request, 'App_login/login_page.html', context=content)


def logout_system(request):
    logout(request)
    return HttpResponseRedirect(reverse('App_product:home'))


@login_required
def profile(request):
    try:
        IsSeller = SellerModel.objects.get(seller=request.user)
    except:
        IsSeller = None

    cart = Cart.objects.filter(user=request.user, purchased=False)

    try:
        user = Profile.objects.get(user=request.user)
    except:
        user = None
    form = ProfileForm(instance=user)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            print("Form is valid")
            this_form = form.save(commit=False)
            this_form.user = request.user
            this_form.save()
            return HttpResponseRedirect(reverse('App_login:profile'))
    orders = Order.objects.filter(user=request.user, ordered=True).order_by('-created')
    content = {
        'form': form,
        'user_profile': user,
        'orders': orders,
        'IsSeller': IsSeller,
        'cart_item': cart.count(),
    }
    return render(request, 'App_login/profile.html', context=content)


def contact_us(request):
    try:
        IsSeller = SellerModel.objects.get(seller=request.user)
    except:
        IsSeller = None

    try:
        cart = Cart.objects.filter(user=request.user, purchased=False).count()
    except:
        cart = 0
    form = ContactUsForm()
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('App_product:home'))
    content = {
        'form': form,
        'IsSeller': IsSeller,
        'cart_item': cart,
    }
    return render(request, 'contact.html', context=content)


@login_required
def become_a_seller(request):
    form = SellerForm()
    if request.method == 'POST':
        form = SellerForm(data=request.POST)
        if form.is_valid():
            this_form = form.save(commit=False)
            this_form.seller = request.user
            shop_name = form.cleaned_data.get('shop_name')
            this_form.shop_id = re.sub(r'[^\w\s]', '', shop_name).replace(" ", "-") + "-" + str(uuid.uuid4())
            this_form.save()
            return HttpResponseRedirect(reverse('App_login:profile'))
    content = {
        'form': form,
    }
    return render(request, 'App_login/become_seller.html', context=content)


def about(request):
    try:
        IsSeller = SellerModel.objects.get(seller=request.user)
    except:
        IsSeller = None
    try:
        cart = Cart.objects.filter(user=request.user, purchased=False).count()
    except:
        cart = 0
    content = {
        'IsSeller': IsSeller,
        'cart_item': cart,
    }
    return render(request, 'App_login/about.html', context=content)
