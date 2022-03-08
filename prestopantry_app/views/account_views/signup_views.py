from django.contrib.auth import login
from django.shortcuts import render, redirect
from prestopantry_app.models.users import User
from prestopantry_app.backends.user_auth import UserAuthBackend

def signup(request):
    content = {}
    if request.method == 'POST':
      email = request.POST['email']
      username = request.POST['username']
      password = request.POST['pwd']
      # Email, username(display name) and password validation HERE (see examples below)
      if (UserAuthBackend.email_taken(email)):
        content['error'] = 'Email already taken'
      if (UserAuthBackend.username_taken(username)):
        content['error'] = 'Username already taken'
      if len(password) < 8:
        content['error'] = 'Password must be at least 8 characters long'
      # Create and log user in if no validation errors
      if content == {}:
        user = User.objects.create_user(username, email, password)
        user.save()
        login(request, user)
    return render(request, 'signup.html', content)
