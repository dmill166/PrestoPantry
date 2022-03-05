# from operator import index
from unicodedata import name
from django.urls import path
from .views import main_views

# urlpatterns = [
#     path('', main_views.home, name='home'),
#     path('about/', main_views.about, name='about'),
#     # path('index/', main_views.index, name='index'),
#     path('apicall/', main_views.apicall, name='apicall'),
#     path('search/', main_views.search, name='search'),
# ]

urlpatterns = [
    path('', main_views.community, name='home'),
    path('landing-page/', main_views.landing_page, name='landing_page'),
    path('signup/', main_views.signup, name='signup'),
    path('login/', main_views.login, name='login'),
    path('logout/', main_views.logout_view, name='logout'),
    path('about/', main_views.about, name='about'),
]