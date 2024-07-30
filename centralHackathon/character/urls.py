# urls.py
from django.urls import path
from .views import timer_page, create_character, history_page, detailed_history, character_missing, watch_ad, deco

urlpatterns = [
    path('timer/', timer_page, name='timer_page'),
    path('create_character/', create_character, name='create_character'),
    path('history/', history_page, name='history_page'),
    path('detailed_history/', detailed_history, name='detailed_history'),
    path('character_missing/', character_missing, name='character_missing'), 
    path('watch_ad/', watch_ad, name='watch_ad'), 
    path('deco/', deco, name='deco'),
]