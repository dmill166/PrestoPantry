from prestopantry_app.backends.spoonacular_api import SpoonacularAPI
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required(login_url='login')
def search_by_ingredient(request):
      if request.method == 'POST' and 'ingredient_button' in request.POST:

        payload = { 
          'ingredients': [request.POST['ingredient_name']], 
          'servings': 1 
          }
        json_scraper = SpoonacularAPI()

        response = json_scraper.ingredient_request("POST", data=str(payload))
        ingredient_json = response.json()
        if response.status_code == 200 and ingredient_json != []:
          context = json_scraper.harvest_ingredients(ingredient_json)
      
          return render(request, 'pantry_ingredients_page.html', {'context': context})

      elif request.method == 'POST' and 'ingredient_per_recipe_button' in request.POST:
    
        # Whether to maximize used ingredients ranking:1 or minimize missing ingredients ranking:2 first.
        payload = {
          'ingredients':[request.POST['ingredients']],
          'number':5,
          'ignorePantry':'false',
          'ranking':2
          }

        response = json_scraper.recipe_request("GET", params=payload)
        recipe_json = response.json()
        if response.status_code == 200 and recipe_json != []:

          context = json_scraper.harvest_recipe_per_ingredients(recipe_json)

          return render(request, 'pantry_ingredients_page.html', {'recipe_context': context})
      
      return render(request, 'pantry_ingredients_page.html', {})