from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('App_login.urls')),
    path('', include('App_product.urls')),
    path('order/', include('App_order.urls')),
    path('payment/', include('App_payment.urls')),
    path('blogs/', include('App_blog.urls')),
    path('app-admin/', include('App_admin.urls')),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
