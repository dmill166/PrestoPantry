from django.test import TestCase
from dynamic_preferences.registries import global_preferences_registry
from prestopantry_app.backends.spoonacular_api import SpoonacularAPI
from googleapiclient.errors import HttpError
from unittest.mock import patch, Mock

ingredient_payload = {

    'image': 'garlic-powder.png', 
    'ingredient_info': [(None, 'Garlic Powder', 872421, '842441131321')], 
    'ingredient_name': 'garlic powder'
    }

recipe_payload = [(
        719320,
        '20 Celebration ! + $500 GIVEAWAY',
        'https://spoonacular.com/recipeImages/719320-312x231.png', 
    [
        (1037063,'breakfast links','https://spoonacular.com/cdn/ingredients_100x100/breakfast-sausage-links.jpg')
    ], 
    [
        (9003,'apple','https://spoonacular.com/cdn/ingredients_100x100/apple.jpg')
    ],
    [
        (20081,'flour','https://spoonacular.com/cdn/ingredients_100x100/flour.png'),
        (18338,'dough','https://spoonacular.com/cdn/ingredients_100x100/filo-dough.png')
    ]
        )]

ingredient_json = [{"original": "garlic powder", "originalName": "garlic powder", "ingredientImage": "garlic-powder.png", "meta": ["garlic_powder"], "products": [{"id": 872421, "upc": "842441131321", "title": "Garlic Powder"}, {"id": 664943, "upc": "033844906801", "title": "Badia Garlic Powder 16 oz (6 count)"}, {"id": 650645, "upc": "072670030410", "title": "Vitarroz Vr Garlic Powder 2.5 Oz"}, {"id": 545593, "upc": "810034763020", "title": "Burma Spice Garlic Powder | Fine Grind | Useful Flavor Enhancer 4.25 lbs."}, {"id": 1945057, "upc": "072728050537", "title": "La Cena Pure Garlic Powder, 10.5 oz"}, {"id": 988431, "upc": "593911450816", "title": "Sprouts Organic Garlic Powder, 2.33 OZ"}, {"id": 511463, "upc": "walmart_product_591397872", "title": "C.F. Sauer Foods Garlic Powder, 5.25 Pound -- 3 per case."}, {"id": 515825, "upc": "769203013377", "title": "Salute Seasonings Garlic Powder 11.75 oz."}, {"id": 623005, "upc": "walmart_product_509766831", "title": "Pride of India- Organic Garlic Powder 3 oz (85.02 Gms)"}, {"id": 959675, "upc": "852659356171", "title": "Marshalls Creek Spices XL GARLIC POWDER REFILL (fine)"}, {"id": 1039137, "upc": "305279313470", "title": "(3 Pack) Pride Of India Organic Garlic Powder 3 Oz"}, {"id": 734105, "upc": "650415756100", "title": "Marshalls Creek Spices (3 PACK) GARLIC POWDER GRANULATED"}, {"id": 1977141, "upc": "654322257392", "title": "Frontier Natural Products, Organic Garlic Powder, 2.33 oz(pack of 6)"}, {"id": 507209, "upc": "654322257361", "title": "Frontier Natural Products, Organic Garlic Powder, 2.33 oz(pack of 2)"}, {"id": 600001, "upc": "842432122956", "title": "Garlic Powder"}, {"id": 410904, "upc": "052500005283", "title": "Sauer's Garlic Powder Ground"}, {"id": 540825, "upc": "052500006419", "title": "Sauer's Ground Garlic Powder, 5.5 oz"}, {"id": 541517, "upc": "052100006260", "title": "McCormick Classic Garlic Powder, 3.12 oz"}, {"id": 698241, "upc": "078742131764", "title": "Great Value Organic Garlic Powder, 2.5 oz"}, {"id": 195537, "upc": "030684898914", "title": "Lawry's Coarse Ground Garlic Powder With Parsley, 5.5 oz (Pack of 12)"}]}]

recipe_json = [{"id": 719320, "title": "20 Celebration ! + $500 GIVEAWAY", "image": "https://spoonacular.com/recipeImages/719320-312x231.png", "imageType": "png", "usedIngredientCount": 1, "missedIngredientCount": 1, "missedIngredients": [{"id": 1037063, "amount": 1.0, "unit": "serving", "unitLong": "serving", "unitShort": "serving", "aisle": "Meat", "name": "breakfast links", "original": "breakfast, Popular", "originalName": "breakfast, Popular", "meta": [], "image": "https://spoonacular.com/cdn/ingredients_100x100/breakfast-sausage-links.jpg"}], "usedIngredients": [{"id": 9003, "amount": 1.0, "unit": "serving", "unitLong": "serving", "unitShort": "serving", "aisle": "Produce", "name": "apple", "original": "Apple, Crock Pot, dessert, Popular", "originalName": "Apple, Crock Pot, dessert, Popular", "meta": [], "image": "https://spoonacular.com/cdn/ingredients_100x100/apple.jpg"}], "unusedIngredients": [{"id": 20081, "amount": 1.0, "unit": "serving", "unitLong": "serving", "unitShort": "serving", "aisle": "Baking", "name": "flour", "original": "flour", "originalName": "flour", "meta": [], "image": "https://spoonacular.com/cdn/ingredients_100x100/flour.png"}, {"id": 18338, "amount": 1.0, "unit": "serving", "unitLong": "serving", "unitShort": "serving", "aisle": "Refrigerated;Frozen", "name": "dough", "original": "dough", "originalName": "dough", "meta": [], "image": "https://spoonacular.com/cdn/ingredients_100x100/filo-dough.png"}], "likes": 105}, {"id": 2481, "title": "Journal", "image": "https://spoonacular.com/recipeImages/2481-312x231.jpg", "imageType": "jpg", "usedIngredientCount": 1, "missedIngredientCount": 1, "missedIngredients": [{"id": 14037, "amount": 1.0, "unit": "serving", "unitLong": "serving", "unitShort": "serving", "aisle": "Alcoholic Beverages", "name": "light rum", "original": "light-meals", "originalName": "light-meals", "meta": [], "image": "https://spoonacular.com/cdn/ingredients_100x100/rum-dark.jpg"}], "usedIngredients": [{"id": 18338, "amount": 1.0, "unit": "serving", "unitLong": "serving", "unitShort": "serving", "aisle": "Refrigerated;Frozen", "name": "filo pastry", "original": "Spinach & Feta Filo Pastry Pies", "originalName": "Spinach & Feta Filo Pastry Pies", "meta": [], "image": "https://spoonacular.com/cdn/ingredients_100x100/filo-dough.png"}], "unusedIngredients": [{"id": 9003, "amount": 1.0, "unit": "serving", "unitLong": "serving", "unitShort": "serving", "aisle": "Produce", "name": "apple", "original": "apple", "originalName": "apple", "meta": [], "image": "https://spoonacular.com/cdn/ingredients_100x100/apple.jpg"}, {"id": 20081, "amount": 1.0, "unit": "serving", "unitLong": "serving", "unitShort": "serving", "aisle": "Baking", "name": "flour", "original": "flour", "originalName": "flour", "meta": [], "image": "https://spoonacular.com/cdn/ingredients_100x100/flour.png"}], "likes": 33}, {"id": 987595, "title": "Apple Ginger Kombucha Cocktail", "image": "https://spoonacular.com/recipeImages/987595-312x231.jpg", "imageType": "jpg", "usedIngredientCount": 1, "missedIngredientCount": 1, "missedIngredients": [{"id": 11216, "amount": 60.0, "unit": "ml", "unitLong": "milliliters", "unitShort": "ml", "aisle": "Produce;Ethnic Foods;Spices and Seasonings", "name": "ginger", "original": "2 30ml GT's Organic Ginger Kombucha, chilled", "originalName": "GT's Organic Ginger Kombucha, chilled", "meta": ["organic", "chilled"], "image": "https://spoonacular.com/cdn/ingredients_100x100/ginger.png"}], "usedIngredients": [{"id": 9003, "amount": 30.0, "unit": "ml", "unitLong": "milliliters", "unitShort": "ml", "aisle": "Produce", "name": "apple", "original": "1 30ml Schonauer Apple Liquor (or apple schnapps or apple jack), chilled", "originalName": "Schonauer Apple Liquor (or apple schnapps or apple jack), chilled", "meta": ["chilled", "(or apple schnapps or apple jack)"], "image": "https://spoonacular.com/cdn/ingredients_100x100/apple.jpg"}], "unusedIngredients": [{"id": 20081, "amount": 1.0, "unit": "serving", "unitLong": "serving", "unitShort": "serving", "aisle": "Baking", "name": "flour", "original": "flour", "originalName": "flour", "meta": [], "image": "https://spoonacular.com/cdn/ingredients_100x100/flour.png"}, {"id": 18338, "amount": 1.0, "unit": "serving", "unitLong": "serving", "unitShort": "serving", "aisle": "Refrigerated;Frozen", "name": "dough", "original": "dough", "originalName": "dough", "meta": [], "image": "https://spoonacular.com/cdn/ingredients_100x100/filo-dough.png"}], "likes": 17}, {"id": 579275, "title": "Apple Cheddar Biscuits", "image": "https://spoonacular.com/recipeImages/579275-312x231.jpg", "imageType": "jpg", "usedIngredientCount": 2, "missedIngredientCount": 2, "missedIngredients": [{"id": 1021009, "amount": 1.0, "unit": "cup", "unitLong": "cup", "unitShort": "cup", "aisle": "Cheese", "name": "extra sharp cheddar cheese", "original": "1 cup extra sharp cheddar cheese, grated", "originalName": "extra sharp cheddar cheese, grated", "meta": ["grated"], "image": "https://spoonacular.com/cdn/ingredients_100x100/cheddar-cheese.png"}, {"id": 1053, "amount": 1.0, "unit": "cup", "unitLong": "cup", "unitShort": "cup", "aisle": "Milk, Eggs, Other Dairy", "name": "heavy cream", "original": "1 cup heavy cream (or any milk you have)", "originalName": "heavy cream (or any milk you have)", "meta": ["or any milk you have)"], "image": "https://spoonacular.com/cdn/ingredients_100x100/fluid-cream.jpg"}], "usedIngredients": [{"id": 9003, "amount": 1.0, "unit": "cup", "unitLong": "cup", "unitShort": "cup", "aisle": "Produce", "name": "apple", "original": "1 apple, chopped (about 1 cup)", "originalName": "apple, chopped (about", "meta": ["chopped"], "image": "https://spoonacular.com/cdn/ingredients_100x100/apple.jpg"}, {"id": 20129, "amount": 2.0, "unit": "cups", "unitLong": "cups", "unitShort": "cup", "aisle": "Baking", "name": "self rising flour", "original": "2 cups self rising flour", "originalName": "self rising flour", "meta": [], "image": "https://spoonacular.com/cdn/ingredients_100x100/flour.png"}], "unusedIngredients": [{"id": 18338, "amount": 1.0, "unit": "serving", "unitLong": "serving", "unitShort": "serving", "aisle": "Refrigerated;Frozen", "name": "dough", "original": "dough", "originalName": "dough", "meta": [], "image": "https://spoonacular.com/cdn/ingredients_100x100/filo-dough.png"}], "likes": 144}, {"id": 1084627, "title": "How to make hot cross buns", "image": "https://spoonacular.com/recipeImages/1084627-312x231.jpg", "imageType": "jpg", "usedIngredientCount": 2, "missedIngredientCount": 2, "missedIngredients": [{"id": 9431, "amount": 1.0, "unit": "serving", "unitLong": "serving", "unitShort": "serving", "aisle": "Produce", "name": "fruit", "original": "The dough will rise much better without the fruit, so only add this after the first rise.", "originalName": "The dough will rise much better without the fruit, so only add this after the first rise", "meta": [], "image": "https://spoonacular.com/cdn/ingredients_100x100/mixed-fresh-fruit.jpg"}, {"id": 98940, "amount": 1.0, "unit": "balls", "unitLong": "ball", "unitShort": "balls", "aisle": "Bakery/Bread", "name": "sub buns", "original": "Shape the buns into smooth balls by tucking the dough into a central point, then turn the buns over so the smoothest surface is on top.", "originalName": "Shape the buns into smooth by tucking the dough into a central point, then turn the buns over so the smoothest surface is on top", "meta": [], "image": "https://spoonacular.com/cdn/ingredients_100x100/french-rolls.jpg"}], "usedIngredients": [{"id": 18338, "amount": 10.0, "unit": "", "unitLong": "", "unitShort": "", "aisle": "Refrigerated;Frozen", "name": "filo dough", "original": "Kneading will take around 10 mins by hand, or five in a table-top mixer. The dough should feel stretchy and bouncy when it's ready.", "originalName": "Kneading will take around mins by hand, or five in a table-top mixer. The dough should feel stretchy and bouncy when it's ready", "meta": [], "image": "https://spoonacular.com/cdn/ingredients_100x100/filo-dough.png"}, {"id": 20081, "amount": 1.0, "unit": "serving", "unitLong": "serving", "unitShort": "serving", "aisle": "Baking", "name": "flour", "original": "Make sure the flour paste for the crosses isn't too runny. You want it thick enough to stay in a straight line on top of the buns.", "originalName": "Make sure the flour paste for the crosses isn't too runny. You want it thick enough to stay in a straight line on top of the buns", "meta": ["thick", "for the crosses isn't too runny. you want it  enough to stay in a straight line on top of the buns. "], "image": "https://spoonacular.com/cdn/ingredients_100x100/flour.png"}], "unusedIngredients": [{"id": 9003, "amount": 1.0, "unit": "serving", "unitLong": "serving", "unitShort": "serving", "aisle": "Produce", "name": "apple", "original": "apple", "originalName": "apple", "meta": [], "image": "https://spoonacular.com/cdn/ingredients_100x100/apple.jpg"}], "likes": 1}]

class SpoonacularApiTest(TestCase):

    def setUp(self):
        self.maxDiff = None
        global ingredient_json
        global ingredient_payload
        global recipe_json
        global recipe_payload

        with patch('google_images_search.GoogleImagesSearch.search', side_effect=HttpError(Mock(status=404), 'not found'.encode())) as googMock:
            self.ingredient_scraper = SpoonacularAPI.harvest_ingredients(ingredient_json)

        self.recipe_scraper = SpoonacularAPI.harvest_recipe_per_ingredients(recipe_json)
        self.spoon_api = SpoonacularAPI

    def test_ingredient_harvester_for_image(self):
        image_json = self.ingredient_scraper['image']
        image_payload = ingredient_payload['image']
        self.assertEqual(image_json, image_payload)
    
    def test_ingredient_harvester_for_name(self):
        name_json = self.ingredient_scraper['ingredient_name']
        name_payload = ingredient_payload['ingredient_name']
        self.assertEqual(name_json, name_payload)


    def test_ingredient_harvester_for_info(self):
        info_json = self.ingredient_scraper['ingredient_info'][0]
        info_payload = ingredient_payload['ingredient_info'][0]
        for i in range(1, len(info_json) - 1):
            self.assertEqual(info_json[i], info_payload[i])

    def test_google_image_for_none(self):
        self.assertIsNone(self.ingredient_scraper['ingredient_info'][0][0])

    def test_recipe_harvester_for_id(self):
        id_json = self.recipe_scraper['recipe'][0][0]
        id_payload = recipe_payload[0][0]
        self.assertEqual(id_json, id_payload)

    def test_recipe_harvester_for_name(self):
        name_json = self.recipe_scraper['recipe'][0][1]
        name_payload = recipe_payload[0][1]
        self.assertEqual(name_json, name_payload)

    def test_recipe_harvester_for_image(self):
        image_json = self.recipe_scraper['recipe'][0][2]
        image_payload = recipe_payload[0][2]
        self.assertEqual(image_json, image_payload)

        # missed used unused 
    def test_recipe_harvester_for_missed_ingredients(self):
        missed_json = self.recipe_scraper['recipe'][0][3]
        missed_payload = recipe_payload[0][3]
        for i in range(len(missed_json) - 1):
            self.assertEqual(missed_json[i], missed_payload[i])

    def test_recipe_harvester_for_used_ingredients(self):
        used_json = self.recipe_scraper['recipe'][0][4]
        used_payload = recipe_payload[0][4]
        for i in range(len(used_json) - 1):
            self.assertEqual(used_json[i], used_payload[i])

    def test_recipe_harvester_for_unused_ingredients(self):
        unused_json = self.recipe_scraper['recipe'][0][5]
        unused_payload = recipe_payload[0][5]
        for i in range(len(unused_json) - 1):
            self.assertEqual(unused_json[i], unused_payload[i])
    
    def test_google_image_setting(self):
        global_preferences = global_preferences_registry.manager()

        with patch('google_images_search.GoogleImagesSearch.search', side_effect=HttpError(Mock(status=404), 'not found'.encode())) as googMock:
            # Test setting off
            global_preferences['google_custom_search_api_enabled'] = False
            SpoonacularAPI.harvest_ingredients(ingredient_json)
            googMock.assert_not_called()

            # Test setting on
            global_preferences['google_custom_search_api_enabled'] = True
            SpoonacularAPI.harvest_ingredients(ingredient_json)
            googMock.assert_called()
