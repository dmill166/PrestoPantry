from django import forms
from django.contrib.auth.forms import UserCreationForm
from prestopantry_app.backends.user_auth import UserAuthBackend
from prestopantry_app.models.users import User
from django.contrib.auth import  password_validation
from django.utils.translation import gettext, gettext_lazy as _



class SignupForm(UserCreationForm):
    username = forms.CharField(label="Display Name", widget=forms.TextInput(attrs={'class': 'form-control huge'}))


    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control huge'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control huge'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    email = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control huge'})
    )
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')

    # Clean functions are called when the form is submitted
    def clean_username(self):
        # Check if username is taken - more validation would go here
        username = self.cleaned_data['username']
        if (UserAuthBackend().username_taken(username)):
            raise forms.ValidationError("Username already taken")
        return username

    def clean_email(self):
        # Check if email is taken - UserCreationForm does rest of validation
        email = self.cleaned_data['email']
        if (UserAuthBackend().email_taken(email)):
            raise forms.ValidationError("Email already taken")
        return email
