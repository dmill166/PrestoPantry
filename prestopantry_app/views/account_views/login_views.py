from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect
from prestopantry_app.backends.user_auth import UserAuthBackend

def login(request):
    if request.method == 'POST':
      email = request.POST['email']
      password = request.POST['pwd']
      user = UserAuthBackend.authenticate(request, email=email, password=password)
      if user:
        auth_login(request, user)
        return redirect('/')
      else:
        return render(request, 'login.html', {'error': 'Invalid email or password'})
    return render(request, 'login.html')
