from django.urls import path
from .views import timer_page, create_character, history_page, detailed_history, character_missing, watch_ad, deco, claim_reward, character_lost_forever

urlpatterns = [
    path('timer/', timer_page, name='timer_page'),
    path('create_character/', create_character, name='create_character'),
    path('history/', history_page, name='history_page'),
    path('detailed_history/', detailed_history, name='detailed_history'),
    path('character_missing/', character_missing, name='character_missing'),
    path('watch_ad/', watch_ad, name='watch_ad'),
    path('deco/', deco, name='deco'),
    path('claim_reward/', claim_reward, name='claim_reward'),
    path('character_lost_forever/', character_lost_forever, name='character_lost_forever'),
]
