from django import forms
from django.contrib.auth.forms import UserCreationForm
from prestopantry_app.backends.user_auth import UserAuthBackend
from prestopantry_app.models.users import User


class SignupForm(UserCreationForm):
    username = forms.CharField(label="Display Name", max_length=50)

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
