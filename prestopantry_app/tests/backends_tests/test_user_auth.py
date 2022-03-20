from django.test import TestCase
from django.contrib.auth import get_user_model
from prestopantry_app.backends.user_auth import UserAuthBackend
from prestopantry_app.models.users import User


class UserAuthTests(TestCase):
    def test_authenticate(self):
        # User does not exist
        self.assertIsNone(UserAuthBackend().authenticate(None, email="test1@gmail.com", password="test_password"))

        # User exists
        User.objects.create_user(username='test_user', email="test1@gmail.com", password="test_password")
        auth_user = UserAuthBackend().authenticate(None, email="test1@gmail.com", password="test_password")
        UserModel = get_user_model()
        db_user = UserModel.objects.get(email="test1@gmail.com")
        self.assertEqual(auth_user, db_user)

        # Invalid password
        self.assertIsNone(UserAuthBackend().authenticate(None, email="test1@gmail.com", password="password"))

    def test_email_taken(self):
        # Email does not exist
        self.assertFalse(UserAuthBackend().email_taken("test1@gmail.com"))

        # Email exists
        User.objects.create_user(username='test_user', email="test1@gmail.com", password="test_password")
        self.assertTrue(UserAuthBackend().email_taken("test1@gmail.com"))

    def test_username_taken(self):
        # Username does not exist
        self.assertFalse(UserAuthBackend().username_taken("test_user"))

        # Username exists
        User.objects.create_user(username='test_user', email="test1@gmail.com", password="test_password")
        self.assertTrue(UserAuthBackend().username_taken("test_user"))
