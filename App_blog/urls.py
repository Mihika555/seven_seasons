from django.urls import path
from App_blog import views

app_name = 'App_blog'

urlpatterns = [
    path('blog-writing/', views.blog_writing, name='blog_writing'),
    path('blog-details/<pk>/', views.blog_details, name='blog-details'),
    path('blogs/', views.show_blogs, name='blogs'),
]
