from prestopantry_app.backends.spoonacular_api import SpoonacularAPI
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.template.response import TemplateResponse
from django.views.decorators.http import require_http_methods
from prestopantry_app.models.user_ingredients import UserIngredient

#Left for reference for searching for recipes PLEASE DELETE THIS AFTER IMPLIMENTING RECIPE SEARCH

def search_recipes(request):
    json_scraper = SpoonacularAPI()

    if request.method == 'POST' and 'search_recipe_button' in request.POST:

        # Whether to maximize used ingredients ranking:1 or minimize missing ingredients ranking:2 first.
        payload = {
          'ingredients':[request.POST['ingredients']],
          'number':2,
          'ignorePantry':'false',
          'ranking':1
          }

        response = json_scraper.recipe_request("GET", params=payload)
        recipe_json = response.json()
        if response.status_code == 200 and recipe_json != []:

            context = json_scraper.harvest_recipe_per_ingredients(recipe_json)

            return render(request, 'recipe_results.html', {'recipe_context': context})

    return render(request, 'recipe_results.html', {'error': 'No results found, please check spelling and try again'})