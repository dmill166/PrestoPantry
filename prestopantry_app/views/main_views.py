from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.template import loader
# Create your views here.

def landing_page(request):
    return render(request, 'landing_page.html')

@login_required(login_url='landing_page')
def community(request):
    return render(request, 'community.html')

def logout_view(request):
    logout(request)
    return render(request, 'logout.html')
