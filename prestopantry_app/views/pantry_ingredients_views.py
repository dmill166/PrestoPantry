from prestopantry_app.backends.spoonacular_api import SpoonacularAPI
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.views.decorators.http import require_http_methods
from prestopantry_app.models.user_ingredients import UserIngredient
from django.urls import reverse

@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def search_pantry_ingredients(request):
    context = {'error': 'No results found, please check spelling and try again'}
    if request.method == 'POST':
        if 'ingredient_button' in request.POST:
            if request.user.allow_api_call():
                response = search_ingredient(request)
                if response:
                    return response
            else:
                context = request.session['ingredient_search_results'] if 'ingredient_search_results' in request.session else context
                context['api_frequency'] = 'Woah, slow down there. Please wait and try again.'
        elif 'add_ingredient_button' in request.POST:
            return add_ingredient(request)
    return TemplateResponse(request, 'search_pantry_ingredients.html', context)


def search_ingredient(request):
    payload = {
        'ingredients': [request.POST['ingredient_name']],
        'servings': 1
        }

    response = SpoonacularAPI.ingredient_request(request="POST", data=str(payload))
    if response and response.status_code == 200:
        ingredient_json = response.json()
        if ingredient_json != []:
            context = SpoonacularAPI.harvest_ingredients(ingredient_json)
            request.session['ingredient_search_results'] = context

            return TemplateResponse(request, 'search_pantry_ingredients.html', context)
    else:
        return TemplateResponse(request, 'search_pantry_ingredients.html', {'error': 'Search Error'})


def add_ingredient(request):
    obj = UserIngredient.objects
    try:
        ingredient = obj.get(user=request.user, ingredient_id=int(request.POST['ingredient_id']))
        ingredient_added = False
    except UserIngredient.DoesNotExist:
        ingredient = obj.create(user=request.user, ingredient_id=int(request.POST['ingredient_id']),
                                ingredient_name=request.POST['ingredient_name'], upc=int(request.POST['upc']))
        ingredient_added = True


    session_ingredient_info = request.session['ingredient_search_results']['ingredient_info']
    for i in session_ingredient_info:
        if i[2] == ingredient.ingredient_id:
            i.append(ingredient_added)
            new_ingredient_search_results = request.session['ingredient_search_results']
            new_ingredient_search_results['ingredient_info'] = session_ingredient_info
            request.session['ingredient_search_results'] = new_ingredient_search_results
            break

    return TemplateResponse(request, 'search_pantry_ingredients.html', request.session['ingredient_search_results'])

#Left for reference for searching for recipes PLEASE DELETE THIS AFTER IMPLIMENTING RECIPE SEARCH

# def search_by_ingredient(request):
#     json_scraper = SpoonacularAPI()

#     elif request.method == 'POST' and 'ingredient_per_recipe_button' in request.POST:

#         # Whether to maximize used ingredients ranking:1 or minimize missing ingredients ranking:2 first.
#         payload = {
#           'ingredients':[request.POST['ingredients']],
#           'number':5,
#           'ignorePantry':'false',
#           'ranking':2
#           }

#         response = json_scraper.recipe_request("GET", params=payload)
#         recipe_json = response.json()
#         if response.status_code == 200 and recipe_json != []:

#             context = json_scraper.harvest_recipe_per_ingredients(recipe_json)

#             return render(request, 'search_pantry_ingredients.html', {'recipe_context': context})

#     return render(request, 'search_pantry_ingredients.html', {'error': 'No results found, please check spelling and try again'})


@login_required(login_url='login')
def display_pantry(request):
    ingredients = UserIngredient.objects.filter(user=request.user)
    context = {'ingredients': ingredients}
    return TemplateResponse(request, 'pantry.html', context) 

def delete_ingredient(request, delete_id):
    try:
        ingredient_delete = UserIngredient.objects.get(ingredient_id=delete_id)
        ingredient_delete.delete()
    except UserIngredient.DoesNotExist:
        pass

    return display_pantry(request)

def delete_all_ingredients(request):
    UserIngredient.objects.filter(user=request.user).delete()
    return display_pantry(request)
