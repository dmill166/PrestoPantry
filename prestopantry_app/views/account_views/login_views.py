from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect
from prestopantry_app.backends.user_auth import UserAuthBackend

def login(request):
    content = {}
    if request.method == 'POST':
      email = request.POST['email']
      password = request.POST['pwd']
      # Email validation HERE 
      # same validation that's used in signup (doesn't change functionality but shouldn't ping the database with an invalid email)
      user = UserAuthBackend.authenticate(request, email=email, password=password)
      if user:
        auth_login(request, user)
        return redirect('/')
      else:
        content['error'] = 'Invalid email or password'
    return render(request, 'login.html', content)
