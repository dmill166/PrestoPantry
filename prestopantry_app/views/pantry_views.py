
from prestopantry_app.backends.spoonacular_api import JsonScraper
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required(login_url='login')
def search_by_ingredient(request):
      if request.method == 'POST' and 'ingredient_button' in request.POST:

        payload = { 
          'ingredients': [request.POST['ingredient_name']], 
          'servings': 1 
          }

        response = JsonScraper.ingredient_request("POST", data=str(payload))
        ingredient_json = response.json()
        context = JsonScraper.harvest_ingredients(ingredient_json)
      
        return render(request, 'pantry_page.html', {'context': context})

      if request.method == 'POST' and 'ingredient_per_recipe_button' in request.POST:
    
        # Whether to maximize used ingredients ranking:1 or minimize missing ingredients ranking:2 first.
        payload = {
          'ingredients':[request.POST['ingredients']],
          'number':5,
          'ignorePantry':'false',
          'ranking':1
          }

        response = JsonScraper.recipe_request("GET", params=payload)
        recipe_json = response.json()
        context = JsonScraper.harvest_recipe_per_ingredients(recipe_json)

        return render(request, 'pantry_page.html', {'recipe_context': context})
      else:
        return render(request, 'pantry_page.html', {})

