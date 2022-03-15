from django.test import TestCase
from prestopantry_app.models.users import User

class SignupViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', email="test1@gmail.com", password='test_password')
    def test_signup_view(self):
        # Get request
        response = self.client.get('/signup/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')
        # Post request
        response = self.client.post('/signup/')
        response.user = self.user
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')



