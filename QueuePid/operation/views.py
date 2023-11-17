from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from .models import *
from login.models import User_info
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Operation
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
    print(request.user)
    operate = Operation.objects.get(customer_username = request.user.username)
    group = request.user.groups.filter(name='Customer').exists()
    timezone_now = timezone.now()
    time_diff = timezone_now - operate.date

    return render(request,'customer_status.html',{'operation':operate,'time_diff':time_diff,'minute_diff': time_diff.seconds // 60,'hour_diff': time_diff.seconds // 60//60, \
                                                  'group':group
                                                  })

def get_number_of_customer(request):

    if request.method == 'POST':

        book = Booking.objects.create(customer_username=request.user,restaurant=request.POST['restaurant_name'],number_of_customer=request.POST['number'])
        user = User_info.objects.get(username=request.user)
        user.book = restaurant=request.POST['restaurant_name']
        book.save()
        user.save()

        return render(request,'customer_status.html')

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
        user.book = None
        operation_user.delete()
        user_queueman.save()
        user.save()
        return customer_complete(request)
    return render(request,'customer_payment.html',{'operation':operation_user,'price':60 + 25*(minute // 25),'credit':user.credit})

def customer_complete(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    return render(request,'customer_complete.html')

    
def customer_review(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    return render(request,'customer_review.html')

def customer_report(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    return render(request,'customer_report.html')
