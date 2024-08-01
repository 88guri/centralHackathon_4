from django.urls import path
from .views import signup, signup_success, join_page, login_page, main_page, home_page, send_verification_email, verify_code
from django.shortcuts import redirect

def home_redirect(request):
    return redirect('/login')

urlpatterns = [
    path('', home_redirect),
    path('signup/', signup, name='signup'),
    path('signup/success/', signup_success, name='signup_success'),
    path('join/', join_page, name='join'),
    path('login/', login_page, name='login'),
    path('main/', main_page, name='main'),
    path('home/', home_page, name='home'),
    path('send_verification_email/', send_verification_email, name='send_verification_email'),
    path('verify_code/', verify_code, name='verify_code'),
]
