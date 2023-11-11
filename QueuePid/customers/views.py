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
import re

def is_valid_email(email):
    # Define the regular expression pattern for a simple email format
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    
    # Use re.match to check if the email matches the pattern
    match = re.match(pattern, email)
    
    # Return True if there is a match, indicating a valid email format
    return bool(match)

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

def edit_page(request,message = "None"):
    # Get the current user's profile (replace with your logic to get the user's profile)
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    user_profile = User_info.objects.get(username=request.user)  
    print(message)
    return render(request,'customer_edit_profile.html',{'user_profile': user_profile,'message':message})

def success_edit(request):
    if request.method == 'POST':
        user_info = User_info.objects.get(username=request.user)
        all_user_info_instances = User_info.objects.all()
        all_usernames = []
        all_emails = []
    
        for i in all_user_info_instances:
            if i.username.username != user_info.username.username :
                all_usernames.append(i.username.username)
            if i.email != user_info.email:
                all_emails.append(i.email)

        if (request.POST['username'] in all_usernames):
            return edit_page(request,message='username already use')

        if ((not is_valid_email(request.POST['email'])) or (request.POST['email'] in all_emails)):
            return edit_page(request,message='this email has already been used')

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