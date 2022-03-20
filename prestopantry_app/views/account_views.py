from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from prestopantry_app.forms.login_form import LoginForm
from prestopantry_app.forms.signup_form import SignupForm
from prestopantry_app.forms.edit_account_forms import EditNameForm, EditUsernameForm, EditEmailForm


def login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.user_cache)
            return redirect('/')
    return render(request, 'login.html', {'form': form})


def signup(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
    return render(request, 'signup.html', {'form': form})


@login_required(login_url='/login')
def edit_account(request):
    context = {}
    forms = [EditUsernameForm(instance=request.user), EditEmailForm(instance=request.user), EditNameForm(instance=request.user), PasswordChangeForm(request.user)]
    if request.method == 'POST':
        if 'username' in request.POST:
            forms[0] = EditUsernameForm(request.POST, instance=request.user)
            if forms[0].is_valid():
                forms[0].save()
                context['success_msg'] = 'Username updated successfully'
        elif 'email' in request.POST:
            forms[1] = EditEmailForm(request.POST, instance=request.user)
            if forms[1].is_valid():
                forms[1].save()
                context['success_msg'] = 'Email updated successfully'
        elif 'first_name' and 'last_name' in request.POST:
            forms[2] = EditNameForm(request.POST, instance=request.user)
            if forms[2].is_valid():
                forms[2].save()
                context['success_msg'] = 'Name updated successfully'
        elif 'old_password' and 'new_password1' and 'new_password2' in request.POST:
            forms[3] = PasswordChangeForm(request.user, request.POST)
            if forms[3].is_valid():
                user = forms[3].save()
                auth_login(request, user)
                context['success_msg'] = 'Password updated successfully'
    context['forms'] = forms
    return render(request, 'account.html', context)
