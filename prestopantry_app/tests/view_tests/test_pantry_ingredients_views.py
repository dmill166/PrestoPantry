from django.test import TestCase
from django.urls import reverse
from prestopantry_app.models.users import User
from prestopantry_app.models.user_ingredients import UserIngredient


class PantryIngredientsViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('goldmember','drevil@gmail.com','ilovegold')
    
    def test_my_pantry_view(self):
        self.client.force_login(self.user)
        response = self.client.get('/pantry/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pantry.html')

    def test_search_by_ingredient_view(self):
        # login
        self.client.force_login(self.user)
        # go to pantry search page
        response = self.client.get(reverse('search-pantry-ingredients'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_pantry_ingredients.html')

        # test search
        data = {'q': '88'}
        response = self.client.get(reverse('search-pantry-ingredients'), data)
        self.assertContains(response, 'No Searches found...')

        # # test add
        session = self.client.session
        session.update({'ingredient_search_results': {'ingredient_info': [['Torkelson Cheese Co. Brick Cheese Wisconsin', 406181, 123344564378]]}})
        session.save()
        data = {'ingredient_name': 'Torkelson Cheese Co. Brick Cheese Wisconsin',
                'ingredient_id': '406181', 'add_ingredient_button': '', 'upc': '123344564378'}
        response = self.client.post('/search-pantry-ingredients/', data)
        self.assertEqual(response.status_code, 200)
        try:
            ingredient=UserIngredient.objects.get(ingredient_name='Torkelson Cheese Co. Brick Cheese Wisconsin',
                                                  ingredient_id='406181', user=self.user, upc=123344564378)
        except UserIngredient.DoesNotExist:
            self.fail("Ingredient failed to save." + str(data))
        self.assertTrue(self.client.session['ingredient_search_results']['ingredient_info'][0][3])

    def test_my_pantry_ingredients_view(self):
        response = self.client.get(reverse('pantry'))
        self.assertRedirects(response, '/login/?next=/pantry/')
         # login
        self.client.force_login(self.user)
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
        self.assertEqual(response.context['ingred'].all().get(), ingredient)

