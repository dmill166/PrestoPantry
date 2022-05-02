from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.base import TemplateView
from .views.account_views import login, signup, edit_account
from .views import main_views, pantry_ingredients_views

urlpatterns = [
    path('', main_views.landing_page, name='landing_page'),
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('account/', edit_account, name='account'),
    path('logout/', main_views.logout_view, name='logout'),
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
    path('pantry/', pantry_ingredients_views.display_pantry, name='pantry'),
    path('pantry/delete=<int:delete_id>', pantry_ingredients_views.delete_ingredient, name='pantry'),
    path('pantry/delete-all', pantry_ingredients_views.delete_all_ingredients, name='delete'),
    path('search-pantry-ingredients/', pantry_ingredients_views.search_pantry_ingredients, name='search-pantry-ingredients'),
    path('auth/', include('social_django.urls', namespace='social')),
    path('search-recipes/', pantry_ingredients_views.search_recipes, name='search-recipes'),
    ]

urlpatterns += staticfiles_urlpatterns()
