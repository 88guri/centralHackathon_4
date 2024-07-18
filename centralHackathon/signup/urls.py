from django.urls import path
from .views import signup, signup_success, join_page, login_page, main_page, home_page

urlpatterns = [
    path('signup/', signup, name = 'signup'),
    path('signup/success', signup_success, name = 'signup_success'),
    path('join/',join_page, name='join'),
    path('login/',login_page, name='login'),
    path('main/', main_page, name='main'),
    path('home/', home_page, name='home'),
]