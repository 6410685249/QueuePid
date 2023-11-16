from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from login.models import User_info
from .models import Queueman
from django.contrib.auth import update_session_auth_hash
from django.db.models import Q
from operation.models import *
from django.utils import timezone
from operation.models import Booking
# Create your views here.
from queueman.models import *
from django.contrib.auth.models import User



def qhome(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    clist = Booking.objects.all()
    queueman = Queueman.objects.get(username = request.user.id)

    request.user
    if request.method == 'POST':
        print(request.POST['customer'])
        print(request.POST['restaurant'])
        return get_queue(request,request.POST['customer'],request.POST['restaurant'])

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
    
    if request.method == 'POST':
        queueman = Queueman.objects.get(username = request.user.id)
        queueman.username.username = request.POST['username'] 
        queueman.phone_number = request.POST['phone_number'] 
        queueman.line_id = request.POST['line_id'] 

        queueman.username.save()
        queueman.save()
        return HttpResponseRedirect(reverse('qprofile'))

    queueman = Queueman.objects.get(username = request.user.id)
    return render(request, 'queueman_edit_profile.html',{
        'queueman':queueman
    })

def change_password(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    if request.method == 'POST':
        new_password = request.POST['password']
        queueman = request.user
        queueman.set_password(new_password)
        queueman.save()
        update_session_auth_hash(request,queueman)
        return HttpResponseRedirect(reverse('logout'))
    
    return render(request,'queueman_change_password.html')


def get_queue(request,customer,restaurant_name):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    user = User.objects.get(username=customer)
    customer_book = Booking.objects.get(customer_username=user)
    customer_book.delete()
    op = Operation.objects.create(customer_username=customer, restaurant=restaurant_name, queueMan_username = request.user.username, \
                                  cost=0,number_Queue= 10,status= 0,update_status=0,date = timezone.now(),number_of_customer=customer_book.number_of_customer
                                  )
    op.save()

    return render(request,'customer_status.html')