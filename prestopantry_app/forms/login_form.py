from django import forms
from django.contrib.auth.forms import AuthenticationForm
from prestopantry_app.backends.user_auth import UserAuthBackend


class LoginForm(AuthenticationForm):
    email = forms.EmailField(max_length=254)
    field_order = ['email', 'password']

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super(AuthenticationForm, self).__init__(*args, **kwargs)
        self.fields.pop('username')

    def clean(self):
        if 'email' in self.cleaned_data:
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if email and password:
                self.user_cache = UserAuthBackend().authenticate(self.request, email, password)
                if self.user_cache is None:
                    raise forms.ValidationError(
                        self.error_messages['invalid_login'], code='invalid_login')
                else:
                    self.confirm_login_allowed(self.user_cache)
        return self.cleaned_data
