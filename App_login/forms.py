from django.forms import ModelForm
from App_login.models import User, Profile, ContactUsModel, SellerModel
from django.contrib.auth.forms import UserCreationForm


# forms
class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ('user', )


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2',)


class ContactUsForm(ModelForm):
    class Meta:
        model = ContactUsModel
        fields = "__all__"


class SellerForm(ModelForm):
    class Meta:
        model = SellerModel
        exclude = ['seller', 'shop_id', 'verified', ]
