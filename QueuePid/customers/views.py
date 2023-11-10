from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
# Create your views here.
from django.contrib.auth import login
from django.shortcuts import render, redirect
# Create your views here.
from .models import Restaurant,Historically
from login.models import User_info
from login.views import logout_view

def list_restaurant(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    return render(request, 'customer_home.html', {'form': [(i.name,i.location) for i in Restaurant.objects.all()]})

def about(request): # render to html
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    return render(request,'customer_about.html')

def wallet(request): # render to html
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    return render(request,'customer_wallet.html')

def account(request): # render to html
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    user = User_info.objects.get(username=request.user)
    return render(request,'customer_account.html',{'user':user})

def edit_page(request):
    # Get the current user's profile (replace with your logic to get the user's profile)
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    user_profile = User_info.objects.get(username=request.user)  
    return render(request,'customer_edit_profile.html',{'user_profile': user_profile})

def success_edit(request):
    if request.method == 'POST':

        user_info = User_info.objects.get(username=request.user)
        user_info.username.username = request.POST['username']
        user_info.username.save()
        user_info.name = request.POST['name']
        user_info.surname = request.POST['surname']
        user_info.email = request.POST['email']
        user_info.telephone = request.POST['tele_phone']

        user_info.save()
        return account(request)
    return edit_page(request)

def change_password(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    return render(request,'customer_change_password.html')


def success_password(request):
    if request.method == 'POST':
        new_password = request.POST['password']
        user = request.user
        user.set_password(new_password)
        user.save() 

        return logout_view(request)
    return change_password(request)


def history(request): # render to html
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    return render(request,'customer_history.html',{'history': [i for i in Historically.objects.filter(username=request.user)]})