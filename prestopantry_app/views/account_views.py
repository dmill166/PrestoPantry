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
    context = {'pass_form': PasswordChangeForm(request.user)}
    if request.method == 'GET':
        if 'change_username' in request.GET:
            context['username_form'] = EditUsernameForm(instance=request.user)
        elif 'change_email' in request.GET:
            context['email_form'] = EditEmailForm(instance=request.user)
        elif 'change_name' in request.GET:
            context['name_form'] = EditNameForm(instance=request.user)
    elif request.method == 'POST':
        request, context = edit_account_post(request, context)
    return render(request, 'account.html', context)


def edit_account_post(request, context):
    if 'username' in request.POST:
        context['username_form'] = EditUsernameForm(request.POST, instance=request.user)
        if context['username_form'].is_valid():
            context['username_form'].save()
            context['success_msg'] = 'Username updated successfully'
    elif 'email' in request.POST:
        context['email_form'] = EditEmailForm(request.POST, instance=request.user)
        if context['email_form'].is_valid():
            context['email_form'].save()
            context['success_msg'] = 'Email updated successfully'
    elif 'first_name' and 'last_name' in request.POST:
        context['name_form'] = EditNameForm(request.POST, instance=request.user)
        if context['name_form'].is_valid():
            context['name_form'].save()
            context['success_msg'] = 'Name updated successfully'
    elif 'old_password' and 'new_password1' and 'new_password2' in request.POST:
        context['pass_form'] = PasswordChangeForm(request.user, request.POST)
        if context['pass_form'].is_valid():
            user = context['pass_form'].save()
            auth_login(request, user)
            context['success_msg'] = 'Password updated successfully'
    return request, context
