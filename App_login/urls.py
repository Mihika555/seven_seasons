from django.urls import path
from App_login import views

app_name = 'App_login'


urlpatterns = [
    path('signup/', views.signup_system, name='signup'),
    path('login/', views.login_system, name='login'),
    path('logout/', views.logout_system, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('contact-us/', views.contact_us, name='contact-us'),
    path('become-a-seller', views.become_a_seller, name='become-seller'),
    path('about/', views.about, name='about'),

]

