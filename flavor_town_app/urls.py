from operator import index
from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('index/', views.index, name='index'),
    path('apicall/', views.apicall, name='apicall'),
    path('search/', views.search, name='search'),
]