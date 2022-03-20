from django.contrib.auth.forms import PasswordChangeForm
from django.test import TestCase
from prestopantry_app.forms.edit_account_forms import EditUsernameForm, EditEmailForm, EditNameForm
from prestopantry_app.models.users import User


class EditUsernameFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user1', email='test1@gmail.com', password='test_password')
        self.client.force_login(self.user)
        self.form = EditUsernameForm({'username': 'test_user'}, instance=self.user)

    def test_clean(self):
        # Username not taken (valid)
        self.assertTrue(self.form.is_valid())

        # Username taken
        User.objects.create_user(username='test_user2', email='test2@gmail.com', password='test_password')
        form_invalid = EditUsernameForm({'username': 'test_user2'}, instance=self.user)
        self.assertFalse(form_invalid.is_valid())

    def test_save(self):
        # Updates username
        self.form.save()
        self.assertEqual(self.user, User.objects.get(username='test_user'))
        self.assertRaises(User.DoesNotExist, User.objects.get, username='test_user1')


class EditEmailFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user1', email='test1@gmail.com', password='test_password')
        self.client.force_login(self.user)
        self.form = EditEmailForm({'email': 'test@gmail.com'}, instance=self.user)

    def test_clean(self):
        # Email not taken (valid)
        self.assertTrue(self.form.is_valid())

        # Email taken
        User.objects.create_user(username='test_user2', email='test2@gmail.com', password='test_password')
        form_invalid = EditEmailForm({'email': 'test2@gmail.com'}, instance=self.user)
        self.assertFalse(form_invalid.is_valid())

    def test_save(self):
        # Updates email
        self.form.save()
        self.assertEqual(self.user, User.objects.get(email="test@gmail.com"))
        self.assertRaises(User.DoesNotExist, User.objects.get, email='test1@gmail.com')


class EditNameFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user1', email='test1@gmail.com', password='test_password')
        self.client.force_login(self.user)
        self.form = EditNameForm({'first_name': 'test_first_name', 'last_name': 'test_last_name'}, instance=self.user)

    def test_clean(self):
        self.assertTrue(self.form.is_valid())

    def test_save(self):
        # Updates name
        self.form.save()
        self.assertEqual(self.user.first_name, self.form.cleaned_data['first_name'])
        self.assertEqual(self.user.last_name, self.form.cleaned_data['last_name'])


class PasswordChangeFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user1', email='test1@gmail.com', password='test_password')
        self.client.force_login(self.user)
        self.form = PasswordChangeForm(self.user, {'old_password': 'test_password', 'new_password1': 'test_password_new', 'new_password2': 'test_password_new'})

    def test_clean(self):
        self.assertTrue(self.form.is_valid())

        form_invalid = PasswordChangeForm(self.user, {'old_password': 'test_password_wrong', 'new_password1': 'test_password_new', 'new_password2': 'test_password_new'})
        self.assertFalse(form_invalid.is_valid())

        form_invalid = PasswordChangeForm(self.user, {'old_password': 'test_password', 'new_password1': 'test_password_new', 'new_password2': 'test_password_new_wrong'})
        self.assertFalse(form_invalid.is_valid())

    def test_save(self):
        # Updates password
        self.form.is_valid()
        self.form.save()
        self.assertFalse(self.user.check_password(self.form.cleaned_data['old_password']))
        self.assertTrue(self.user.check_password(self.form.cleaned_data['new_password1']))
