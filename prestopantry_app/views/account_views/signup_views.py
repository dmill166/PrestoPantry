from django.contrib.auth import login
from django.shortcuts import render, redirect
from prestopantry_app.models.users import User
from prestopantry_app.backends.user_auth import UserAuthBackend

def signup(request):
    if request.method == 'POST':
      email = request.POST['email']
      username = request.POST['username']
      password = request.POST['pwd']
      # Email, username(display name) and password validation HERE
      if (UserAuthBackend.email_taken(email)):
        return render(request, 'signup.html', {'error': 'Email already taken'})
      if (UserAuthBackend.username_taken(username)):
        return render(request, 'signup.html', {'error': 'Username already taken'})
      user = User.objects.create_user(username, email, password)
      user.save()
      login(request, user)
      return render(request, 'signup.html')
    else:
        return render(request, 'signup.html')