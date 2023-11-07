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
    user = User_info.objects.get(username=request.user)
    
    return render(request,'customer_account.html',{'user':user})

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

def edit_profile(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    from django.shortcuts import render, redirect


def edit_profile(request):
    # Get the current user's profile (replace with your logic to get the user's profile)
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    user_profile = User_info.objects.get(username=request.user)  # Assuming you have a foreign key relationship to User
    return render(request,'customer_edit_profile.html',{'user_profile': user_profile})


def go_to_edit_profile_page(request):
    if request.method == 'POST':
        return edit_profile(request)
    return account(request)

def in_edit_back_account(request):
    if request.method == 'POST':
        return account(request)
    return edit_profile(request)

def in_success_edit_back_account(request):
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
    return edit_profile(request)

def go_to_change_password_page(request):
    if request.method == 'POST':
        return change_password(request)
    return account(request)

def change_password(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    return render(request,'customer_change_password.html')

def in_change_password_back_to_account(request):
    
    if request.method == 'POST':
        return account(request)
    return change_password(request)

def complete_password(request):
    if request.method == 'POST':
        new_password = request.POST['password']
        user = request.user
        user.set_password(new_password)
        user.save() 

        return logout_view(request)
    return change_password(request)
