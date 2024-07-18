from django.urls import path
from .views import home_page

urlpatterns = [
    path('homee/', home_page, name='homee'),
]
