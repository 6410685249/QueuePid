from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render,redirect
from .models import *
from login.models import User_info
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Operation
from django.utils import timezone
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
        book = Booking.objects.create(customer_username=request.user,restaurant=request.POST['restaurant_name'],number_of_customer=request.POST['number'])
        user = User_info.objects.get(username=request.user)
        operate = Operation.objects.create(customer_username=request.user,restaurant=request.POST['restaurant_name'],status=0)
        user.book = restaurant=request.POST['restaurant_name']
        book.save()
        user.save()

        return redirect('customer_status')
