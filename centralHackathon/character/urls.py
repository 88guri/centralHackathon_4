from django.urls import path
from .views import timer_page, create_character, history_page

urlpatterns = [
    path('timer/', timer_page, name='timer_page'),
    path('create_character/', create_character, name='create_character'),
    path('history/', history_page, name='history_page'),
]
