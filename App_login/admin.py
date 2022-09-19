from django.contrib import admin
from App_login.models import Profile, User, ContactUsModel, SellerModel

# Register your models here.
admin.site.register(User)
admin.site.register(Profile)
admin.site.register(ContactUsModel)
admin.site.register(SellerModel)
