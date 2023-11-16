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
total_seconds = 0

def booking(request, restaurant_name):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    return render(request, 'customer_booking.html',{'restaurant':restaurant_name})

def customer_status(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login')) 
    print(request.user.username)
    operate = Operation.objects.get(customer_username = request.user.username)
    timezone_now = timezone.now()
    print(operate.date)
    print(timezone_now)
    print(operate.date - timezone_now)
    return render(request,'customer_status.html',{'operation':operate,'timezone_now':timezone_now})

def get_number_of_customer(request):

    if request.method == 'POST':

        book = Booking.objects.create(customer_username=request.user,restaurant=request.POST['restaurant_name'],number_of_customer=request.POST['number'])
        user = User_info.objects.get(username=request.user)
        user.book = restaurant=request.POST['restaurant_name']
        book.save()
        user.save()

        return render(request,'customer_status.html')
    
def capture_time(request):
    # Get the current time from the AJAX request data
    data = request.body.decode('utf-8')
    current_time = json.loads(data).get('current_time')

    # Process the captured time as needed
    print('Captured Time:', current_time)

    # Respond with a success message
    return JsonResponse({'message': 'Time captured successfully'}) 

# def get_timer(request):
#     global total_seconds
#     return JsonResponse({'total_seconds': total_seconds})