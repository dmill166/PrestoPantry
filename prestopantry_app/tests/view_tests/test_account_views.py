from django.test import TestCase
from prestopantry_app.forms.edit_account_forms import EditUsernameForm, EditNameForm, EditEmailForm
from prestopantry_app.models.users import User
from unittest.mock import patch


class LoginViewTests(TestCase):
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


class EditAccountViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', email="test1@gmail.com", password='test_password')

    def test_edit_account_view(self):
        # Get request
        # No user logged in
        response = self.client.get('/account/')
        self.assertEqual(response.status_code, 302)
        # User logged in
        self.client.force_login(self.user)
        response = self.client.get('/account/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account.html')

        # Post requests
        # Valid Username Form
        with patch('prestopantry_app.views.account_views.EditUsernameForm.is_valid') as form_mock:
            response = self.client.post('/account/', {'username': 'test_user1'})
            form_mock.assert_called_once()
            self.assertEqual(response.status_code, 200)
            self.assertNotIn('username_form', response.context)

        # Invalid Username Form
        with patch('prestopantry_app.views.account_views.EditUsernameForm.is_valid') as form_mock:
            form_mock.return_value = False
            response = self.client.post('/account/', {'username': 'test_user1_invalid!@#$%^&*()'})
            form_mock.assert_called_once()
            self.assertEqual(response.status_code, 200)
            self.assertIsInstance(response.context['username_form'], EditUsernameForm)

        # Valid Email Form
        with patch('prestopantry_app.views.account_views.EditEmailForm.is_valid') as form_mock:
            response = self.client.post('/account/', {'email': 'test1_new@gmail.com'})
            form_mock.assert_called_once()
            self.assertEqual(response.status_code, 200)
            self.assertNotIn('email_form', response.context)

        # Invalid Email Form
        with patch('prestopantry_app.views.account_views.EditEmailForm.is_valid') as form_mock:
            form_mock.return_value = False
            response = self.client.post('/account/', {'email': 'test1_new_invalid@gma'})
            form_mock.assert_called_once()
            self.assertEqual(response.status_code, 200)
            self.assertIsInstance(response.context['email_form'], EditEmailForm)

        # Valid Name Form
        with patch('prestopantry_app.views.account_views.EditNameForm.is_valid') as form_mock:
            response = self.client.post('/account/', {'first_name': 'testFirstName', 'last_name': 'testLastName'})
            form_mock.assert_called_once()
            self.assertEqual(response.status_code, 200)
            self.assertNotIn('name_form', response.context)

        # Invalid Name Form
        with patch('prestopantry_app.views.account_views.EditNameForm.is_valid') as form_mock:
            form_mock.return_value = False
            response = self.client.post('/account/', {'first_name': 'testFirstNameInvalid1', 'last_name': 'testLastNameInvalid1'})
            form_mock.assert_called_once()
            self.assertEqual(response.status_code, 200)
            self.assertIsInstance(response.context['name_form'], EditNameForm)

        with patch('django.contrib.auth.forms.PasswordChangeForm.is_valid') as form_mock:
            form_mock.return_value = False
            response = self.client.post('/account/', {'old_password': 'test_password', 'new_password1': 'test_password_new', 'new_password2': 'test_password_new'})
            form_mock.assert_called_once()
            self.assertEqual(response.status_code, 200)
