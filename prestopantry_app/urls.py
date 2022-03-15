# from operator import index
from unicodedata import name
from django.urls import path

from .views.account_views import signup_views, login_views
from .views import main_views

urlpatterns = [
    path('', main_views.community, name='home'),
    path('landing-page/', main_views.landing_page, name='landing_page'),
    path('signup/', signup_views.signup, name='signup'),
    path('login/', login_views.login, name='login'),
    path('logout/', main_views.logout_view, name='logout'),
    path('about/', main_views.about, name='about'),
]