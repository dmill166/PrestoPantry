from prestopantry_app.backends.spoonacular_api import SpoonacularAPI
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from prestopantry_app.models.user_ingredients import UserIngredient

@login_required(login_url='login')
def search_by_ingredient(request):
    json_scraper = SpoonacularAPI()
    if request.method == 'POST' and 'ingredient_button' in request.POST:

        payload = {
          'ingredients': [request.POST['ingredient_name']],
          'servings': 1
          }

        response = json_scraper.ingredient_request(request="POST", data=str(payload))
        if response and response.status_code == 200:
            ingredient_json = response.json()
            if ingredient_json != []:
                context = json_scraper.harvest_ingredients(ingredient_json)
                request.session['ingredient_search_results'] = context

                return render(request, 'search_pantry_ingredients.html', context)
        else:
            return render(request, 'search_pantry_ingredients.html', {'error': 'Search Error'})

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

            return render(request, 'search_pantry_ingredients.html', {'recipe_context': context})

    elif request.method == 'POST' and 'add_ingredient_button' in request.POST:
        obj = UserIngredient.objects
        ingredient = obj.create(user=request.user, ingredient_id=int(request.POST['ingredient_id']),
                                ingredient_name=request.POST['ingredient_name'], upc=int(request.POST['upc']))
        session_ingredient_info = request.session['ingredient_search_results']['ingredient_info']
        for i in session_ingredient_info:
            if i[1] == ingredient.ingredient_id:
                i.append(True)
                new_ingredient_search_results = request.session['ingredient_search_results']
                new_ingredient_search_results['ingredient_info'] = session_ingredient_info
                request.session['ingredient_search_results'] = new_ingredient_search_results
                break

        return render(request, 'search_pantry_ingredients.html', request.session['ingredient_search_results'])

    return render(request, 'search_pantry_ingredients.html', {'error': 'No results found, please check spelling and try again'})

@login_required(login_url='login')
def display_pantry(request):
    ingredients = UserIngredient.objects.filter(user=request.user)
    return render(request, 'pantry.html', {'ingred': ingredients}) 