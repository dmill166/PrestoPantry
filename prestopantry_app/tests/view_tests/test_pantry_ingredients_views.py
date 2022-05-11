from django.test import TestCase
from django.urls import reverse
from dynamic_preferences.registries import global_preferences_registry
from prestopantry_app.models.users import User
from prestopantry_app.models.user_ingredients import UserIngredient
from prestopantry_app.backends.spoonacular_api import SpoonacularAPI
from unittest.mock import patch


class PantryIngredientsViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('goldmember', 'drevil@gmail.com', 'ilovegold')
        self.global_preferences = global_preferences_registry.manager()
        self.global_preferences['time_between_api_calls'] = 0
        self.global_preferences['spoonacular_api_enabled'] = True
        self.client.force_login(self.user)

    def test_my_pantry_view(self):
        self.client.force_login(self.user)
        response = self.client.get('/pantry/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pantry.html')

    def test_search_pantry_ingredients(self):
        # go to pantry search page
        response = self.client.get(reverse('search-pantry-ingredients'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_pantry_ingredients.html')

        # test search page
        self.assertNotContains(response, 'No results found, please check spelling and try again')

        # No results found
        with patch('prestopantry_app.views.pantry_ingredients_views.search_ingredient', return_value=None):
            response = self.client.post(reverse('search-pantry-ingredients'), data={'ingredient_button': ''})
            self.assertContains(response, 'No results found, please check spelling and try again')


        # test spam check
        with patch.object(User, 'allow_api_call', return_value=False):
            response = self.client.post(reverse('search-pantry-ingredients'), {'ingredient_button': '', 'ingredient_name': 'test'})
            self.assertContains(response, 'Woah, slow down there. Please wait and try again.')

    def test_search_ingredient(self):

        with patch('prestopantry_app.backends.spoonacular_api.requests.request') as mock_request:
            # Test when Spoon API is disabled
            self.global_preferences['spoonacular_api_enabled'] = False
            response = self.client.post(reverse('search-pantry-ingredients'), {'ingredient_button': '', 'ingredient_name': 'test'})
            mock_request.assert_not_called()
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'Search Error')

            # Test when Spoon API is enabled
            self.global_preferences['spoonacular_api_enabled'] = True
            response = self.client.post(reverse('search-pantry-ingredients'), {'ingredient_button': '', 'ingredient_name': 'test'})
            mock_request.assert_called_once()
            self.assertEqual(response.status_code, 200)

    def test_add_ingredient(self):
        # test add
        session = self.client.session
        session.update({'ingredient_search_results': {'ingredient_info': [[None, 'Torkelson Cheese Co. Brick Cheese Wisconsin', 406181, 123344564378]]}})
        session.save()
        data = {'ingredient_name': 'Torkelson Cheese Co. Brick Cheese Wisconsin',
                'ingredient_id': '406181', 'add_ingredient_button': '', 'upc': '123344564378'}
        response = self.client.post('/search-pantry-ingredients/', data)
        self.assertEqual(response.status_code, 200)
        try:
            UserIngredient.objects.get(ingredient_name='Torkelson Cheese Co. Brick Cheese Wisconsin',
                                       ingredient_id=406181, user=self.user, upc=123344564378)
        except UserIngredient.DoesNotExist:
            self.fail("Ingredient failed to save." + str(data))

        self.assertTrue(response.context['ingredient_info'][0][4])

        session.delete('ingredient_search_results')
        session.save()
        # test add ingredient already in pantry
        response = self.client.post('/search-pantry-ingredients/', data)
        self.assertFalse(response.context['ingredient_info'][0][4])

    def test_my_pantry_ingredients_view(self):
        # go to pantry search page
        response = self.client.get(reverse('pantry'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pantry.html')

        # test search for empty pantry
        response = self.client.get(reverse('pantry'))
        self.assertContains(response, 'Nothing in pantry')

        # test search for pantry with ingredients
        ingredient = UserIngredient.objects.create(ingredient_name='Torkelson Cheese Co. Brick Cheese Wisconsin',
                                                   ingredient_id='406181', user=self.user, upc=123344564378)
        self.client.force_login(self.user)
        response = self.client.get('/pantry/')
        self.assertEqual(response.context['ingredients'].all().get(), ingredient)

        # test no user
        self.client.logout()
        response = self.client.get(reverse('pantry'))
        self.assertRedirects(response, '/login/?next=/pantry/')

    def test_delete_ingredients(self):
        user2 = User.objects.create_user('djkhalid', 'sufferingfromsuccess@gmail.com', 'anotherone')

        # test delete
        ingredient1 = UserIngredient.objects.create(ingredient_name='Torkelson Cheese Co. Brick Cheese Wisconsin',
                                                   ingredient_id='406181', user=self.user, upc=123344564378)

        ingredient2 = UserIngredient.objects.create(ingredient_name='Torkelson Cheese Co. Brick Cheese Wisconsin',
                                                   ingredient_id='406181', user=user2, upc=123344564378)

        # Check ingredient was added
        self.client.force_login(self.user)
        response = self.client.get('/pantry/')
        self.assertEqual(response.context['ingredients'].all().get(), ingredient1)
        response = self.client.get('/pantry/delete=406181')
        try:
            response.context['ingredients'].all().get()
            self.fail("Expected ingredient to not exist.")
        except UserIngredient.DoesNotExist:
            pass

        self.assertEqual(UserIngredient.objects.get(ingredient_name='Torkelson Cheese Co. Brick Cheese Wisconsin'), ingredient2)

    def test_delete_all(self):
        # test delete all
        ingredient = UserIngredient.objects.create(ingredient_name='Torkelson Cheese Co. Brick Cheese Wisconsin',
                                                   ingredient_id='406181', user=self.user, upc=123344564378)

        ingredient2 = UserIngredient.objects.create(ingredient_name='Hector incredible pizza',
                                                    ingredient_id='12345', user=self.user, upc=123344566543)

        response = self.client.get('/pantry/')
        self.assertEqual(response.context['ingredients'].all().get(ingredient_name='Torkelson Cheese Co. Brick Cheese Wisconsin'), ingredient)
        self.assertEqual(response.context['ingredients'].all().get(ingredient_name='Hector incredible pizza'), ingredient2)

        response = self.client.get('/pantry/delete-all')
        ingredients = UserIngredient.objects.filter(user=self.user)

        self.assertFalse(ingredients.exists())
        self.assertFalse(response.context['ingredients'].exists())

    def test_search_recipes(self):
        session = self.client.session

        # Test search no with no ingredients selected - Display pantry and prompts user to select an ingredient
        session.update({'error': 'Please select at least one ingredient.'})
        session.save()
        response = self.client.get('/search-recipes/')
        self.assertTemplateUsed(response, 'pantry.html')
        self.assertContains(response, 'Please select at least one ingredient')
        self.assertRaises(KeyError, lambda: self.client.session['api_frequency'])
        self.assertNotContains(response, 'No recipes found')
        self.assertNotContains(response, 'Woah, slow down there. Please wait and try again.')

        ingredient = UserIngredient.objects.create(ingredient_name='Torkelson Cheese Co. Brick Cheese Wisconsin',
                                                   ingredient_id='406181', user=self.user, upc=123344564378)
        ingredient2 = UserIngredient.objects.create(ingredient_name='Hector incredible pizza',
                                                    ingredient_id='12345', user=self.user, upc=123344566543)
        ingredient_query = {'select': [ingredient.ingredient_name, ingredient2.ingredient_name]}

        # Test Spoon API to search for recipes is called
        with patch.object(SpoonacularAPI, 'recipe_request') as recipe_request_mock:
            response = self.client.get('/search-recipes/', ingredient_query)
            recipe_request_mock.assert_called_once_with('GET', params={
                    'ingredients': [ingredient.ingredient_name + ', ' + ingredient2.ingredient_name],
                    'number': 5,
                    'ignorePantry': 'false',
                    'ranking': 1
                    }
                )
            self.assertTemplateUsed(response, 'recipe_results.html')
            self.assertNotContains(response, 'Woah, slow down there. Please wait and try again.')

        # Test spoon api disabled - Search Error displayed
        self.global_preferences['spoonacular_api_enabled'] = False
        response = self.client.get('/search-recipes/', ingredient_query)
        self.assertContains(response, 'API Search Error')
        self.assertNotContains(response, 'Woah, slow down there. Please wait and try again.')
        self.assertTemplateUsed(response, 'recipe_results.html')

        # Test api frequency enforcement - Displays pantry page with an api frequency error
        self.global_preferences['time_between_api_calls'] = 5
        session.update({'error': 'Woah, slow down there. Please wait and try again.'})
        session.save()
        response = self.client.get('/search-recipes/', ingredient_query)
        self.assertTemplateUsed(response, 'pantry.html')
        self.assertContains(response, 'Woah, slow down there. Please wait and try again.')
        self.assertRaises(KeyError, lambda: self.client.session['error'])
