# from operator import index
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from .views.account_views import login, signup, edit_account
from .views import main_views, pantry_ingredients_views

urlpatterns = [
    path('', main_views.community, name='home'),
    path('landing-page/', main_views.landing_page, name='landing_page'),
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('account/', edit_account, name='account'),
    path('logout/', main_views.logout_view, name='logout'),
    path('about/', main_views.about, name='about'),
    path('pantry-ingredients/', pantry_ingredients_views.search_by_ingredient, name='pantry-ingredients'),
    path('auth/', include('social_django.urls', namespace='social')),

]

urlpatterns += staticfiles_urlpatterns()
