from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
# Create your views here.
from django.contrib.auth import login
from django.shortcuts import render, redirect
# Create your views here.
from .models import Restaurant,Historically
def list_restaurant(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    restaurant_list = Restaurant.objects.all()
    name_and_location = [(i.name,i.location) for i in Restaurant.objects.all()]
    return render(request, 'customer_home.html', {'form': name_and_location})

def history(request):
    print('IN history fuinc')
    if request.method == 'POST':
        print('IN if history fuinc')
        return history_list(request)
    return list_restaurant(request)

def history_list(request): # render to html
    print('IN if history_list fuinc')
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    return render(request, 'customer_history.html', {'history': Historically.objects.all()})

def in_history_back_to_home(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    if request.method == 'POST':
        return list_restaurant(request)
    return history_list(request)

def go_to_about_page(request):

    if request.method == 'POST':
        return about(request)
    return list_restaurant(request)

def about(request): # render to html
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    return render(request,'customer_about.html')

def in_about_back_to_home(request):

    if request.method == 'POST':
        return list_restaurant(request)
    return about(request)

def wallet(request): # render to html
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    return render(request,'customer_wallet.html')

def go_to_wallet_page(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    if request.method == 'POST':
        return wallet(request)
    return list_restaurant(request)

def in_wallet_back_to_home(request):

    if request.method == 'POST':
        return list_restaurant(request)
    return wallet(request)

def account(request): # render to html
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    return render(request,'customer_account.html')

def go_to_account_page(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    if request.method == 'POST':
        return account(request)
    return list_restaurant(request)

def in_account_back_to_home(request):

    if request.method == 'POST':
        return list_restaurant(request)
    return account(request)