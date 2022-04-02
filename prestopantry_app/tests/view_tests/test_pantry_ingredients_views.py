from django.test import TestCase
from django.urls import reverse
from prestopantry_app.models.users import User
from prestopantry_app.models.user_ingredients import UserIngredient

class PantryIngredientsViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('goldmember','drevil@gmail.com','ilovegold')

    def test_pantry_ingredients_view(self):
        # login
        self.client.login(username='goldmember', email= 'drevil@gmail.com', password='ilovegold')
        # go to pantry search page
        response = self.client.get(reverse('pantry-ingredients'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pantry_ingredients_page.html')
        self.assertContains(response, '<h2>Ingredient Search Central</h2>')

        # test search
        data = {'q': '88'}
        response = self.client.get(reverse('pantry-ingredients'), data)
        self.assertContains(response, 'No Searches found...')

        # # test add
        data = {'ingredient_name': 'Torkelson Cheese Co. Brick Cheese Wisconsin', 
        'ingredient_id': '406181', 'add_ingredient_button': '', 'upc': '123344564378'}
        response = self.client.post('/pantry-ingredients/', data)
        try:
            ingredient=UserIngredient.objects.get(ingredient_name='Torkelson Cheese Co. Brick Cheese Wisconsin',
            ingredient_id='406181', user=self.user, upc=123344564378)
        except UserIngredient.DoesNotExist:
            self.fail("Ingredient failed to save." + str(data))