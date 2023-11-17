from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render,redirect
from customers.models import Historically
from queueman.models import Queueman
from login.models import User_info
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import *
from django.utils import timezone
from queueman.models import *

total_seconds = 0

def booking(request, restaurant_name):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    return render(request, 'customer_booking.html',{'restaurant':restaurant_name})

def customer_status(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login')) 

    operate = Operation.objects.get(customer_username = request.user.username)

    timezone_now = timezone.now()
    if operate.date != None:
        time_diff = timezone_now - operate.date
        return render(request,'customer_status.html',
                      {'operation':operate,'time_diff':time_diff,
                       'minute_diff': time_diff.seconds // 60,'hour_diff': time_diff.seconds // 60//60,
                                                  })
    return render(request,'customer_status.html',
                  {'operation':operate,})

def get_number_of_customer(request):
    if request.method == 'POST':
        book = Booking.objects.create(customer_username=request.user,restaurant=request.POST['restaurant_name'],number_of_customer=int(request.POST['number']))
        user = User_info.objects.get(username=request.user)
        operate = Operation.objects.create(customer_username=request.user,restaurant=request.POST['restaurant_name'],status=0,cost=0,number_of_customer=int(request.POST['number']),update_status="0")
        user.book = restaurant=request.POST['restaurant_name']
        book.save()
        user.save()


        return redirect('customer_status')

def customer_payment(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login')) 
    operation_user = Operation.objects.get(customer_username=request.user.username)
    user = User_info.objects.get(username = request.user)
    queueman = User.objects.get(username=operation_user.queueMan_username)
    user_queueman = Queueman.objects.get(username=queueman)

    time_end = timezone.now()
    time_start = operation_user.date
    time_diff = (time_end - time_start).seconds
    minute = time_diff // 60
    if request.method == "POST":
        user.credit -= 60 + 25*(minute // 25)
        user_queueman.credit +=  int((60 + 25*(minute // 25)) / 2)
        user_queueman.save()
        operation_user.cost = 60 + 25*(minute // 25)
        user.save()
        return render(request,'customer_review.html')
    return render(request,'customer_payment.html',{'operation':operation_user,'price':60 + 25*(minute // 25),'credit':user.credit})

def customer_complete(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    return render(request,'customer_complete.html')

    
def customer_review(request):

    if request.method == "POST":
        op = Operation.objects.get(customer_username = request.user.username)
        user_cus = User.objects.get(username=op.customer_username)
        user_que = User.objects.get(username=op.queueMan_username)
        customer = User_info.objects.get(username = user_cus)
        queueman = Queueman.objects.get(username = user_que)
        review = Review.objects.create(customer_username=op.customer_username, \
                                       queueman_username=op.queueMan_username, \
                                       comment=request.POST['comment'], \
                                       star=int(request.POST['rating'][0])) 
        his = Historically.objects.create(username=op.customer_username,restaurant=op.restaurant , \
                                cost= op.cost,queeuManName=op.queueMan_username,date=op.date,phone_number_QueueMan=customer.telephone,phone_number_customer=queueman.phone_number)
        queueman.star = (queueman.star + int(request.POST['rating'][0])) / 2 ### 4.5 4 4.25
        customer.book = None
        customer.save()
        op.delete()
        return redirect('restaurant_list')
    return render(request,'customer_review.html')

def customer_report(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    return render(request,'customer_report.html')
