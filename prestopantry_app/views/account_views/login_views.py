from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect
from prestopantry_app.forms.login_form import LoginForm


def login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.user_cache)
            return redirect('/')
    return render(request, 'login.html', {'form': form})
