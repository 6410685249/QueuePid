from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
# Create your views here.
from django.contrib.auth import login
from django.shortcuts import render, redirect
# Create your views here.

def list_restaurant(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    print(request.user)
    print(request.user.password)
    return render(request, 'home.html')