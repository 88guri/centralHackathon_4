from django.urls import path
from .views import timer_page

urlpatterns = [
    path('timer/', timer_page, name='timer'),
]
