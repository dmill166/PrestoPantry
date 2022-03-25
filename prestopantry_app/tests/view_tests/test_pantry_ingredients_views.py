from django.test import TestCase
from django.urls import reverse
from prestopantry_app.models.users import User

class PantryIngredientsViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('goldmember','drevil@gmail.com','ilovegold')

    def test_pantry_ingredients_view(self):
        # login
        self.client.login(username='goldmember', email= 'drevil@gmail.com', password='ilovegold')
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        # go to pantry search page
        response = self.client.get(reverse('pantry-ingredients'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pantry_ingredients_page.html')
        self.assertContains(response, '<h2>Ingredient Search Central</h2>')

        # test search
        data = {'q': '88'}
        response = self.client.get(reverse('pantry-ingredients'), data)
        self.assertContains(response, 'No Searches found...')
