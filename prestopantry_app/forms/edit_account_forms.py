from django import forms
from django.contrib.auth.forms import UserChangeForm
from prestopantry_app.models.users import User


class EditUsernameForm(UserChangeForm):
    password = None
    username = forms.CharField(label="Display name", max_length=50)

    class Meta:
        model = User
        fields = ['username']


class EditEmailForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ['email']


class EditNameForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ['first_name', 'last_name']
