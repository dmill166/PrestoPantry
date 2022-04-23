from django.test import TestCase
from django.utils.timezone import now
from dynamic_preferences.registries import global_preferences_registry
from prestopantry_app.models.users import User
from datetime import datetime, timedelta


class UserTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user1', email='test1@gmail.com', password='test_password')

    def test_oauth_user(self):
        user_no_pass = User.objects.create_user(username='test_user_pass', email='test_pass@gmail.com')
        self.assertTrue(user_no_pass.oauth_user())
        user_with_pass = User.objects.create_user(username='test_user_no_pass', email='test_no_pass@gmail.com', password='test_password2')
        self.assertFalse(user_with_pass.oauth_user())

    def test_allow_api_call(self):
        global_preferences = global_preferences_registry.manager()
        time_between_api_calls = global_preferences['time_between_api_calls']

        # User not allowed if it hasn't been longer than time_between_api_calls
        self.user.last_api_call = now()
        self.user.save()
        self.assertFalse(self.user.allow_api_call())

        # User allowed if it has been longer than time_between_api_calls (1.1 is for threshold)
        self.user.last_api_call = now() - timedelta(seconds=time_between_api_calls*1.1)
        self.user.save()
        self.assertTrue(self.user.allow_api_call())

