from django.forms import ModelForm
from django import forms
from App_product.models import FruitModel


class FruitForm(ModelForm):
    seasons = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': "Summer, Rainy-Season, Autumn, Late-Autumn, Winter, Spring"}))

    class Meta:
        model = FruitModel
        exclude = ['vendor', 'availability']
