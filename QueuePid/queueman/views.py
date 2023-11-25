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
import smtplib
from django.views.decorators.csrf import csrf_exempt
from math import radians, cos, sin, asin, sqrt
from customers.models import Restaurant

# Create your views here.

smtp_object = smtplib.SMTP('smtp.gmail.com', 587)
smtp_object.ehlo()
smtp_object.starttls()
email = 'queuepidcorp@gmail.com'
password = 'jvqk fwso vgkq jlvp'

@csrf_exempt
def qhome(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    clist = Booking.objects.all()
    queueman = Queueman.objects.get(username = request.user.id)
    restaurant = []

    for c in clist:
        restaurant.append(Restaurant.objects.get(name = c.restaurant))

    clist = zip(clist,restaurant)

    size = len(restaurant)

    return render(request, 'queueman_home.html',{
                  'clist':clist,
                  'queueman':queueman,
                  'size':size
            })


def wallet(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    
    queueman = Queueman.objects.get(username = request.user.id)
    return render(request, 'queueman_wallet.html',{
                  'queueman':queueman,
    })

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

def get_queue(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    
    queueman = Queueman.objects.get(username = request.user.id)
    
    if request.method == 'POST':
        operate = Operation.objects.get(customer_username = request.POST['customer'])
        user = User.objects.get(username =  request.POST['customer'])
        info = User_info.objects.get(username = user.id)
        customer_book = Booking.objects.get(customer_username=user)
        customer_book.delete()
        operate.queueMan_username = request.user.username
        operate.status += 1
        queueman.is_have_queue =True
        operate.save() 
        queueman.save()

        if info.verify_gmail == True:
            smtp_object.login(email, password)
            msg = 'Subject: ' + 'Update Status' + '\n' + 'On the way'
            smtp_object.sendmail(email, info.email, msg)

        return redirect('qstatus')

def status(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    
    operate = Operation.objects.get(queueMan_username = request.user.username)
    user = User.objects.get(username =  operate.customer_username)
    info = User_info.objects.get(username = user.id)
    queueman = Queueman.objects.get(username = request.user.id)
    alert = 0

    
    if operate.update_status == True:
        queueman.is_have_queue = False
        queueman.save()
        operate.delete()
        return redirect('qhome')
    

    if request.method == 'POST':
        if 'number_queue' in request.POST and request.POST['number_queue'] == '':
            return redirect('qstatus')
        if operate.status == 1:
            operate.status +=1
            operate.number_Queue = request.POST['number_queue']
            operate.date = timezone.now()
            operate.save()
            
            if info.verify_gmail == True:

                msg = 'Subject: ' + 'Update Status' + '\n' + 'In Queue'
                smtp_object.sendmail(email, info.email, msg)
            
            return redirect('qstatus')
        
        elif operate.status == 2 and operate.number_Queue !=0:
            operate.number_Queue = request.POST['number_queue']
            operate.save()
            return redirect('qstatus')
        
        elif operate.status == 2 and operate.number_Queue ==0:
            operate.status +=1
            queueman.is_have_queue = False
            operate.temp = operate.queueMan_username
            operate.queueMan_username = ''
            operate.save()
            queueman.save()

            if info.verify_gmail == True:
                msg = 'Subject: ' + 'Finnish' + '\n' + 'Your queue is finish'
                smtp_object.sendmail(email, info.email, msg)
                smtp_object.quit()
            return redirect('qhome')
        
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

def cancel(request):
    operate = Operation.objects.get(queueMan_username = request.user.username)
    user = User.objects.get(username =  operate.customer_username)
    info = User_info.objects.get(username = user.id)
    queueman = Queueman.objects.get(username = request.user.id)
    operate.update_status = True
    queueman.is_have_queue = False
    operate.save()
    info.save()
    queueman.save()
    return redirect('qhome')

def withdrawn(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    if request.method == 'POST':

        image = request.POST['credit']
        user = Queueman.objects.get(username=request.user)
        user.upload = image
        user.save()
        return redirect(reverse('qwallet'))
    return render(request,'queue_with_drawn.html')

def complete_with_drawn(request):
    if request.method == 'POST':
        print('in queueman')

        user = User.objects.get(username = request.POST['user'])
        user_value = Queueman.objects.get(username = user)
        user_value.upload = 0
        user_value.save()
        return redirect(reverse('admin_page'))

def admin_commit_with_drawn(request):
    if request.method == 'POST':

        user = User.objects.get(username = request.POST['user'])
        user_value = Queueman.objects.get(username = user)
        return render(request,'admin_commit_with_drawn.html',{'credit':user_value.upload,'user':user})