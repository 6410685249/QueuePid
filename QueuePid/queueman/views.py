from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from login.models import User_info
from .models import Queueman

# Create your views here.


def qhome(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    
    clist = User_info.objects.all()
    queueman = Queueman.objects.get(username = request.user.id)

    return render(request, 'queueman_home.html',{
                  'clist':clist,
                  'queueman':queueman,
    })


def wallet(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    
    queueman = Queueman.objects.get(username = request.user.id)
    return render(request, 'queueman_wallet.html',{
                  'queueman':queueman,
    })


def history(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    
    return render(request, 'queueman_history.html')

def profile(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    
    queueman = Queueman.objects.get(username = request.user.id)
    return render(request, 'queueman_profile.html',{
                  'queueman':queueman,
    })

def edit_profile(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    return render(request, 'queueman_edit_profile.html')