from django.test import TestCase
from prestopantry_app.models.users import User


class UserTests(TestCase):
    def test_oauth_user(self):
        user_no_pass = User.objects.create_user(username='test_user1', email='test1@gmail.com')
        self.assertTrue(user_no_pass.oauth_user())
        user_with_pass = User.objects.create_user(username='test_user2', email='test2@gmail.com', password='test_password2')
        self.assertFalse(user_with_pass.oauth_user())
