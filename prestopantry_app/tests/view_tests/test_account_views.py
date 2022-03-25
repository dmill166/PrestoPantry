from django.test import RequestFactory, TestCase
from prestopantry_app.models.users import User
from prestopantry_app.views.account_views import edit_account
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
        self.factory = RequestFactory()

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
        request = self.factory.post('/account/', {'username': 'test_user1'})
        request.user = self.user
        with patch('prestopantry_app.forms.edit_account_forms.EditUsernameForm.is_valid') as form_mock:
            response = edit_account(request)
            form_mock.assert_called()
            self.assertEqual(response.status_code, 200)

        request = self.factory.post('/account/', {'email': 'test1_new@gmail.com'})
        request.user = self.user
        with patch('prestopantry_app.forms.edit_account_forms.EditEmailForm.is_valid') as form_mock:
            response = edit_account(request)
            form_mock.assert_called()
            self.assertEqual(response.status_code, 200)

        request = self.factory.post('/account/', {'first_name': 'testFirstName', 'last_name': 'testLastName'})
        request.user = self.user
        with patch('prestopantry_app.forms.edit_account_forms.EditNameForm.is_valid') as form_mock:
            response = edit_account(request)
            form_mock.assert_called()
            self.assertEqual(response.status_code, 200)

        request = self.factory.post('/account/', {'old_password': 'test_password', 'new_password1': 'test_password_new', 'new_password2': 'test_password_new'})
        request.user = self.user
        with patch('django.contrib.auth.forms.PasswordChangeForm.is_valid') as form_mock:
            form_mock.return_value = False
            response = edit_account(request)
            form_mock.assert_called()
            self.assertEqual(response.status_code, 200)
