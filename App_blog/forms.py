from django import forms
from App_blog.models import NutritionBlogModel


class BlogWritingFrom(forms.ModelForm):
    class Meta:
        model = NutritionBlogModel
        exclude = ['user', ]

