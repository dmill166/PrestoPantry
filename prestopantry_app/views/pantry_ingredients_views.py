from prestopantry_app.backends.spoonacular_api import SpoonacularAPI
from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from django.views.decorators.http import require_http_methods
from prestopantry_app.models.user_ingredients import UserIngredient


@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def search_pantry_ingredients(request):
    context = {}
    if request.method == 'POST':
        if 'ingredient_button' in request.POST:
            if request.user.allow_api_call():
                response = search_ingredient(request)
                if response:
                    return response
                context['error'] = 'No results found, please check spelling and try again'
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
        if ingredient_json != [] and 'products' in ingredient_json[0] and ingredient_json[0]['products'] != []:
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
                                ingredient_name=request.POST['ingredient_name'], upc=request.POST['upc'])
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


@require_http_methods(["GET"])
@login_required(login_url='login')
def search_recipes(request):
    context = {'error': 'No recipes found'}
    ingredients_list = request.GET.getlist('select')
    if ingredients_list:
        if not request.user.allow_api_call():
            request.session['error'] = 'Woah, slow down there. Please wait and try again.'
            return display_pantry(request)
        payload = {
          'ingredients': [', '.join(ingredients_list)],
          'number': 5,
          'ignorePantry': 'false',
          'ranking': 1
          }
        recipe_search_response = SpoonacularAPI.recipe_request("GET", params=payload)
        if recipe_search_response and recipe_search_response.status_code == 200:
            recipe_search_json = recipe_search_response.json()

            if recipe_search_json != []:
                recipes = SpoonacularAPI.harvest_recipe_per_ingredients(recipe_search_json)
                return TemplateResponse(request, 'recipe_results.html', {'recipe_context': recipes})
        else:
            context['error'] = 'API Search Error'
    else:
        request.session['error'] = 'Please select at least one ingredient'
        return display_pantry(request)

    return TemplateResponse(request, 'recipe_results.html', context)


@require_http_methods(["GET"])
@login_required(login_url='login')
def display_pantry(request):
    context = {}
    ingredients = UserIngredient.objects.filter(user=request.user)
    if 'error' in request.session:
        context['error'] = request.session['error']
        del request.session['error']
    context['ingredients'] = ingredients
    return TemplateResponse(request, 'pantry.html', context)


@require_http_methods(["GET"])
@login_required(login_url='login')
def delete_ingredient(request, delete_id):
    try:
        ingredient_delete = UserIngredient.objects.get(user=request.user, ingredient_id=delete_id)
        ingredient_delete.delete()
    except UserIngredient.DoesNotExist:
        pass

    return display_pantry(request)


@require_http_methods(["GET"])
@login_required(login_url='login')
def delete_all_ingredients(request):
    UserIngredient.objects.filter(user=request.user).delete()
    return display_pantry(request)
