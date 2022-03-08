from django.contrib.auth import login
from django.shortcuts import render
from prestopantry_app.forms.signup_form import SignupForm
from prestopantry_app.models.users import User

def signup(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(form.clean_username(), form.clean_email(), form.clean_password())
            login(request, user)
    return render(request, 'signup.html', {'form': form})
