from django.urls import path
from .views import timer_page, create_character

urlpatterns = [
    path('timer/', timer_page, name='timer_page'),
    path('create_character/', create_character, name='create_character'),
]
