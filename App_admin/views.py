from django.contrib.auth.decorators import login_required
from django.shortcuts import render, reverse, redirect
from django.http import HttpResponseRedirect

# Create your views here.
from App_login.models import User, Profile
from App_login.models import SellerModel
from App_order.models import Order
from App_product.models import FruitModel


def admin_checker(user):
    users = User.objects.filter(is_superuser=True)
    if user in users:
        return True
    return False


@login_required
def admin_home(request):
    if admin_checker(request.user):
        verified_stores = SellerModel.objects.filter(verified=True).count()
        requested_stores = SellerModel.objects.filter(verified=False).count()
        all_fruits = FruitModel.objects.filter(availability=True).count()
        total_orders = Order.objects.all().count()
        content = {
            'verified_stores': verified_stores,
            'requested_stores': requested_stores,
            'all_fruits': all_fruits,
            'total_orders': total_orders,
        }
        return render(request, 'App_admin/admin_home.html', context=content)
    else:
        return redirect('App_product:home')


@login_required
def admin_stores(request):
    if admin_checker(request.user):
        stores = SellerModel.objects.filter(verified=True)
        requested_stores = SellerModel.objects.filter(verified=False)
        content = {
            'stores': stores,
            'requested_stores': requested_stores,
        }
        return render(request, 'App_admin/all_stores.html', context=content)
    else:
        return redirect('App_product:home')


@login_required
def verify_store(request, pk):
    store = SellerModel.objects.get(id=pk)
    if request.method == 'GET':
        store.verified = True
        store.save()
    return HttpResponseRedirect(reverse('App_admin:all-stores'))


@login_required
def orders(request):
    total_orders = Order.objects.all().order_by('-created')
    content = {
        'orders': total_orders
    }
    return render(request, 'App_admin/orders.html', context=content)
