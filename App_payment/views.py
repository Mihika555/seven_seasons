from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from sslcommerz_python.payment import SSLCSession

from App_login.models import Profile
from App_order.models import Cart, Order, OrderForVendorModel
from App_payment.forms import BillingForm
from App_payment.models import BillingAddress
from App_login.models import SellerModel
from django.views.decorators.csrf import csrf_exempt


@login_required
def checkout_page(request):
    try:
        IsSeller = SellerModel.objects.get(seller=request.user)
    except:
        IsSeller = None

    saved_address = BillingAddress.objects.get_or_create(user=request.user)
    saved_address = saved_address[0]
    form = BillingForm(instance=saved_address)
    if request.method == 'POST':
        form = BillingForm(request.POST, instance=saved_address)
        if form.is_valid():
            form.save()
            form = BillingForm(instance=saved_address)
            messages.success(request, "Shipping Address Saved!!!")
    carts = Cart.objects.filter(user=request.user, purchased=False)
    fruit_price = 0.0
    for cart in carts:
        my_order = Order.objects.get_or_create(order_item=cart, user=request.user)
        vendor_order = OrderForVendorModel.objects.get_or_create(order_item=cart, user=cart.item.vendor)
        fruit_price += float(cart.get_total())
    vendors = [x.item.vendor for x in carts]
    delivery_charge = len(set(vendors)) * 150

    content = {
        'form': form,
        'saved_address': saved_address,
        'total_price': fruit_price + delivery_charge,
        'delivery_charge': delivery_charge,
        'carts': carts,
        'cart_item': carts.count(),
        'IsSelling': IsSeller,
    }
    return render(request, 'App_Payment/checkout.html', context=content)


@login_required
def payment(request):
    profile = Profile.objects.get(user=request.user)
    saved_address = BillingAddress.objects.get_or_create(user=request.user)
    saved_address = saved_address[0]
    if not saved_address.is_full_filled():
        messages.info(request, f"Please complete shipping address.")
        return redirect('App_Payment:checkout')

    if not profile.is_fully_filled():
        messages.info(request, "Please complete your profile details.")
        return redirect('App_login:profile')

    status_url = request.build_absolute_uri(reverse('App_payment:purchased-complete'))
    mypayment = SSLCSession(sslc_is_sandbox=True, sslc_store_id='mexyz60d96068c3b77',
                            sslc_store_pass='mexyz60d96068c3b77@ssl')
    mypayment.set_urls(success_url=status_url, fail_url=status_url,
                       cancel_url=status_url, ipn_url=status_url)
    order_total = 0
    carts = Cart.objects.filter(user=request.user, purchased=False)
    order_item = carts
    order_item_count = carts.count()
    if request.method == "POST":
        order_total = float(request.POST.get('total_price'))
    mypayment.set_product_integration(total_amount=Decimal(order_total), currency='BDT',
                                      product_category='Fruit',
                                      product_name=order_item, num_of_item=order_item_count, shipping_method='Courier',
                                      product_profile='None')

    current_user = profile
    user_country = str(profile.country)
    saved_country = str(saved_address.country)
    address_1 = f"{current_user.House}, {current_user.city}-{current_user.zipcode}"
    mypayment.set_customer_info(name=current_user.full_name, email=request.user.email,
                                address1=saved_address.address,
                                address2=address_1, city=current_user.city,
                                postcode=current_user.zipcode, country=user_country,
                                phone=str(current_user.phone_number))

    mypayment.set_shipping_info(shipping_to=current_user.full_name, address=saved_address.address,
                                city=saved_address.city_zone, postcode=saved_address.zip_code,
                                country=saved_country)
    response_data = mypayment.init_payment()
    return redirect(response_data['GatewayPageURL'])


@csrf_exempt
def purchased_complete(request):
    print("Purchased")
    if request.method == 'POST':
        payment_data = request.POST
        print(payment_data)
        status = payment_data['status']
        amount = payment_data['amount']
        tran_date = payment_data['tran_date']
        currency = payment_data['currency']
        if status == 'VALID':
            bank_tran_id = payment_data['bank_tran_id']
            tran_id = payment_data['tran_id']
            val_id = payment_data['val_id']
            card_type = payment_data['card_type']
            return HttpResponseRedirect(
                reverse('App_payment:complete-payment', kwargs={'val_id': val_id, 'tran_id': tran_id, }))
        elif status == 'FAILED':
            messages.warning(request, f"Your payment is failed")
        elif status == 'CANCELLED':
            messages.warning(request, "Your payment has been stopped!!!")

    if request.user.is_authenticated:
        cart_item = Cart.objects.filter(user=request.user, purchased=False).count()
    else:
        cart_item = 0
    content = {
        'cart_item': cart_item,
    }
    return render(request, 'App_payment/complete_payment.html', context=content)


def complete_payment(request, val_id, tran_id):
    carts = Cart.objects.filter(user=request.user, purchased=False)
    customer_orders = Order.objects.filter(user=request.user, ordered=False)
    vendor_orders = OrderForVendorModel.objects.filter(order_item__user=request.user, confirmed=False)
    for order in customer_orders:
        order.ordered = True
        order.payment_id = val_id
        order.order_id = tran_id
        order.save()
    for order in vendor_orders:
        order.confirmed = True
        order.payment_id = val_id
        order.order_id = tran_id
        order.save()
    for cart in carts:
        cart.purchased = True
        cart.save()
    return redirect('App_product:home')
