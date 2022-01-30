from operator import le
from django.conf import settings
from flavor_town_app.models import Owner, Question
import django
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from django.template import loader
import requests
# Create your views here.


# def home(request):
#     return HttpResponse("Home page!!")
#     # return render(request, '/home.html'),

def home(request):
    return render(request, 'home.html')

def about(request):
    site_owner_list = Owner.objects.all()
    context = {'site_owner': site_owner_list}
    return render(request, 'about.html', context)

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'index.html', context)

def apicall(request):
    response = requests.get('https://api.spoonacular.com/food/products/search?query=beer&number=4&apiKey=' + settings.API_KEY)
    random_recipe = response.json()
    # print(random_recipe['products'][1]['title'])
    # print(random_recipe['products'][1]['id'])
    # # print(random_recipe['products'][1])
    # print(random_recipe['products'][1]['image'])
    food_arr = []
    for i in range(len(random_recipe['products'])):
        context = {
            'id' : random_recipe['products'][i]['id'],
            'title': random_recipe['products'][i]['title'],
            'image': random_recipe['products'][i]['image'],

        }
        food_arr.append(context)
    print(food_arr)
    return render(request,  'apicall.html', {'stuff' : food_arr})


def search(request):
    if request.method == 'POST':
        # name of the form tag in search.html
        user_searched = request.POST['user_searched']
        response = requests.get('https://api.spoonacular.com/food/products/search?query=' + user_searched + '&number=4&apiKey=' + settings.API_KEY)
        random_recipe = response.json()

        food_arr = []
        for i in range(len(random_recipe['products'])):
            context = {
                'id' : random_recipe['products'][i]['id'],
                'title': random_recipe['products'][i]['title'],
                'image': random_recipe['products'][i]['image'],

            }
            food_arr.append(context)
        return render(request, 'search.html', {'searched': food_arr})
    else:
         return render(request, 'search.html', {})
