from django.test import TestCase
from prestopantry_app.models.users import User

class LoginViewtest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', email="test1@gmail.com", password='test_password')
    def test_login_view(self):
      # Get request
      response = self.client.get('/login/')
      self.assertEqual(response.status_code, 200)
      self.assertTemplateUsed(response, 'login.html')
      # Post request
      response = self.client.post('/login/', {'username': 'test_user', 'email': 'test1@gmail.com', 'password': 'test_password'})
      response.user = self.user
      self.assertEqual(response.status_code, 302)
      self.assertRedirects(response, '/')