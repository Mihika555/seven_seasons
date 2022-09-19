from django.db import models


# Create your models here.
from App_login.models import User


class NutritionBlogModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_author')
    blog_title = models.CharField(max_length=100)
    main_image = models.ImageField(upload_to='blog_images/')
    image1 = models.ImageField(upload_to='blog_images/')
    image2 = models.ImageField(upload_to='blog_images/')
    image3 = models.ImageField(upload_to='blog_images/')
    blog = models.TextField()
    created_date = models.DateTimeField(auto_now=True)
    update_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.blog_title
