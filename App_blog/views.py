from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from App_blog.forms import BlogWritingFrom
from App_blog.models import NutritionBlogModel


# Create your views here.
from App_login.models import SellerModel
from App_order.models import Cart


@login_required
def blog_writing(request):
    try:
        IsSeller = SellerModel.objects.get(seller=request.user)
    except:
        IsSeller = None

    form = BlogWritingFrom()
    cart = Cart.objects.filter(user=request.user, purchased=False)
    if request.method == 'POST':
        form = BlogWritingFrom(request.POST, request.FILES)
        if form.is_valid():
            this_blog = form.save(commit=False)
            this_blog.user = request.user
            this_blog.save()

            return HttpResponseRedirect(reverse('App_blog:blogs'))
    content = {
        'form': form,
        'IsSeller': IsSeller,
        'cart_item': cart.count(),
    }
    return render(request, 'App_blog/blog_writing.html', context=content)


def blog_details(request, pk):
    blog = NutritionBlogModel.objects.get(id=pk)
    content = {
            'blog': blog
    }
    return render(request, 'App_blog/blog_details.html', context=content)


def show_blogs(request):
    all_blogs = NutritionBlogModel.objects.all()
    try:
        IsSeller = SellerModel.objects.get(seller=request.user)
    except:
        IsSeller = None

    try:
        cart = Cart.objects.filter(user=request.user, purchased=False).count()
    except:
        cart = 0
    content = {
        'all_blog': all_blogs,
        'IsSeller': IsSeller,
        'cart_item': cart,
    }
    return render(request, 'App_blog/show_blogs.html', context=content)

