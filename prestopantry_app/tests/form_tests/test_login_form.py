from django.test import TestCase
from prestopantry_app.forms.login_form import LoginForm
from prestopantry_app.models.users import User
from django.contrib.auth import get_user_model

class LoginFormTests(TestCase):
    def test_login_form_authentication(self):
        # Invalid email (no user)
        form_invalid_email = LoginForm({'email': 'test1@gma', 'password': 'test_password'})
        self.assertFalse(form_invalid_email.is_valid())

        # valid email and password (user exists)
        User.objects.create_user(username='test_user', email="test1@gmail.com", password="test_password")
        form_valid = LoginForm(data = {'email': 'test1@gmail.com', 'password': 'test_password'})

        UserModel = get_user_model()    
        self.assertTrue(form_valid.is_valid())
        self.assertEquals(form_valid.user_cache, UserModel.objects.get(email='test1@gmail.com'))

        # Invalid password (user exists)
        form_incorrect_password = LoginForm(data = {'email': 'test1@gmail.com', 'password': 'password'})
        self.assertFalse(form_incorrect_password.is_valid())