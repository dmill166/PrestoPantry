from django.test import TestCase
from prestopantry_app.forms.signup_form import SignupForm
from django.contrib.auth import get_user_model


class SignupFormTests(TestCase):
    def test_clean_username(self):
        # Username does not exist (form.is_valid() should pass)
        form_valid = SignupForm({'username': 'test1', 'email': 'test1@gmail.com', 'password1': 'test_password', 'password2': 'test_password'})
        self.assertTrue(form_valid.is_valid())
        form_valid.save()
        # Username exists (form.is_valid() should fail)
        form_invalid = SignupForm({'username': 'test1', 'email': 'test2@gmail.com', 'password1': 'test_password', 'password2': 'test_password'})
        self.assertFalse(form_invalid.is_valid())

    def test_clean_email(self):
        # Email does not exist (form.is_valid() should pass)
        form_valid = SignupForm({'username': 'test1', 'email': 'test1@gmail.com', 'password1': 'test_password', 'password2': 'test_password'})
        self.assertTrue(form_valid.is_valid())
        form_valid.save()

        # Email exists (form.is_valid() should fail)
        form_invalid = SignupForm({'username': 'test2', 'email': 'test1@gmail.com', 'password1': 'test_password', 'password2': 'test_password'})
        self.assertFalse(form_invalid.is_valid())

    def test_clean_password2(self):
        # Password1 and Password2 match (valid)
        form_valid = SignupForm({'username': 'test1', 'email': 'test1@gmail.com', 'password1': 'test_password', 'password2': 'test_password'})
        self.assertTrue(form_valid.is_valid())

        # Password1 and Password2 do not match (invalid)
        form_invalid = SignupForm({'username': 'test1', 'email': 'test1@gmail.com', 'password1': 'test_password1', 'password2': 'test_password2'})
        self.assertFalse(form_invalid.is_valid())

    def test_save(self):
        # Create and save user (if info valid)
        form = SignupForm({'username': 'test_user', 'email': 'test1@gmail.com', 'password1': 'test_password', 'password2': 'test_password'})
        self.assertTrue(form.is_valid())
        UserModel = get_user_model()
        self.assertEqual(form.save(), UserModel.objects.get(email="test1@gmail.com"))
