from django.test import TestCase
from prestopantry_app.forms.signup_form import SignupForm
from django.contrib.auth import get_user_model


class SignupFormTests(TestCase):
    def test_clean_username(self):
        # Username does not exist (form.is_valid() should pass)
        pass
    
        # Username exists (form.is_valid() should fail)
        pass

    def test_clean_email(self):
        # Email does not exist (form.is_valid() should pass)
        pass
    
        # Email exists (form.is_valid() should fail)
        pass


    def test_save(self):
        # Create and save user (if info valid)
        form = SignupForm({'username': 'test_user', 'email': 'test1@gmail.com', 'password1': 'test_password', 'password2': 'test_password'})
        self.assertTrue(form.is_valid())
        UserModel = get_user_model()    
        self.assertEqual(form.save(), UserModel.objects.get(email="test1@gmail.com"))
        
        # Invalid username (user not created - search by email or username)
        
        # Invalid email (user not created - search by email or username)
        
        # Invalid password (user not created - search by email or username)
        
        # Passwords don't match (user not created - search by email or username)
        


