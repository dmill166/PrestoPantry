# from operator import index
from unicodedata import name
from django.urls import path
from .views import main_views

urlpatterns = [
    path('', main_views.home, name='home'),
    path('about/', main_views.about, name='about'),
    # path('index/', main_views.index, name='index'),
    path('apicall/', main_views.apicall, name='apicall'),
    path('search/', main_views.search, name='search'),
]