from django.contrib.auth import login
from django.shortcuts import render
from prestopantry_app.forms.signup_form import SignupForm


def signup(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
    return render(request, 'signup.html', {'form': form})
