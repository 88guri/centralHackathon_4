from django.urls import path
from .views import (
    create_character, timer_page, history_page, detailed_history,
    character_missing, watch_ad, deco, claim_reward, delete_character,
    watch_ad_reward, watch_ad2
)

urlpatterns = [
    path('timer/', timer_page, name='timer_page'),
    path('create_character/', create_character, name='create_character'),
    path('history/', history_page, name='history_page'),
    path('detailed_history/', detailed_history, name='detailed_history'),
    path('character_missing/', character_missing, name='character_missing'),
    path('watch_ad/', watch_ad, name='watch_ad'),
    path('deco/', deco, name='deco'),
    path('claim_reward/', claim_reward, name='claim_reward'),
    path('delete_character/', delete_character, name='delete_character'),
    path('watch_ad_reward/', watch_ad_reward, name='watch_ad_reward'),
    path('watch_ad2/', watch_ad2, name='watch_ad2'),
]
