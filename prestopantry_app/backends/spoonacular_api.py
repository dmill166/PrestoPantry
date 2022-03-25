from django.conf import settings
import requests

SPOON_API = settings.SPOON_API_KEY

headers = {
    'content-type': "application/json",
    'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
    'x-rapidapi-key': SPOON_API
    }

url1 = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/food/ingredients/map"
url2 = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/findByIngredients"


class SpoonacularAPI():

    def ingredient_request(request, data):
        response = requests.request(request, url1, data=str(data), headers=headers)
        return response

    def recipe_request(request, params):
        response = requests.request(request, url2, params=params, headers=headers)
        return response
        


    def harvest_ingredients(json_file):
        ingredient_name = json_file[0]['originalName']
        image = json_file[0]['ingredientImage']
        products = json_file[0]['products']

        ingredient_tup = ()
        ingredient_arr = []

        for product in products:
          name = product['title']
          id = product['id']
          upc = product['upc']
          ingredient_tup =(name, id, upc)
          ingredient_arr.append(ingredient_tup)

        ingredient_payload = {
            'ingredient_name': ingredient_name ,
            'image': image, 
            'ingredient_info': ingredient_arr,
            }

        return ingredient_payload

    def harvest_recipe_per_ingredients(json_file):

        payload = []

        for dic in json_file:
            missed_tup = ()
            miss_arr = []
            used_tup = ()
            used_arr = []
            unused_tup = ()
            unused_arr = []
            payload_tup = ()

            id = dic['id']
            recipe_title = dic['title']
            image = dic['image']
            missed_ingredients = dic['missedIngredients']
            used_ingredients = dic['usedIngredients']
            unused_ingredients = dic['unusedIngredients']

            for missed in missed_ingredients:
                miss_id = missed['id']
                miss_ing = missed['name']
                miss_ing_image = missed['image']
                missed_tup = (miss_id, miss_ing, miss_ing_image)
                miss_arr.append(missed_tup)

            for used in used_ingredients:
                used_id = used['id'] # used.0
                used_ing = used['name'] # used.6
                used_ing_image = used['image'] # used.10
                used_tup = (used_id, used_ing, used_ing_image)
                used_arr.append(used_tup)

            for unused in unused_ingredients:
                unused_id = unused['id']
                unused_ing = unused['name']
                unused_ing_image = unused['image']
                unused_tup = (unused_id, unused_ing, unused_ing_image)
                unused_arr.append(unused_tup)

            payload_tup = ((id, recipe_title, image, miss_arr, used_arr, unused_arr))
            payload.append(payload_tup)

        recipe_payload = {
          'recipe': payload,
        }

        return recipe_payload
