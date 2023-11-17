from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render,redirect
from .models import Queueman
from django.contrib.auth import update_session_auth_hash
from operation.models import *
from django.utils import timezone
from operation.models import Booking
from queueman.models import *
from django.contrib.auth.models import User
from operation.views import customer_status
# Create your views here.


def qhome(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    clist = Booking.objects.all()
    queueman = Queueman.objects.get(username = request.user.id)

    if request.method == 'POST':
        operate = Operation.objects.get(customer_username = request.POST['customer'])
        user = User.objects.get(username =  request.POST['customer'])
        customer_book = Booking.objects.get(customer_username=user)
        customer_book.delete()
        operate.queueMan_username = request.user.username
        operate.status += 1
        operate.save() 

        return redirect('qstatus')
    
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


def status(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    operate = Operation.objects.get(queueMan_username = request.user.username)

    if request.method == 'POST':
        if operate.status == 1:
            operate.status +=1
            operate.number_Queue = request.POST['number_queue']
            operate.date = timezone.now()
            operate.save()
            return redirect('qstatus')
        elif operate.status == 2 and operate.number_Queue !=0:
            operate.number_Queue = request.POST['number_queue']
            operate.save()
            return redirect('qstatus')
        elif operate.status == 2 and operate.number_Queue ==0:
            operate.status +=1
            operate.save()
            return redirect('qstatus')
        
    if operate.date != None:
        timezone_now = timezone.now()
        time_diff = timezone_now - operate.date
        return render(request,'queueman_status.html',
                      {'operation':operate,
                       'time_diff':time_diff,
                       'minute_diff': time_diff.seconds // 60,
                       'hour_diff': time_diff.seconds // 60//60,
                        })

    return render(request,'queueman_status.html',{
        'operation':operate
    })
