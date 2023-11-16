from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from .models import *
from login.models import User_info

def booking(request, restaurant_name):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    return render(request, 'customer_booking.html',{'restaurant':restaurant_name})

def get_number_of_customer(request):

    if request.method == 'POST':
        print('IN booking')
        print(request.POST)
        book = Booking.objects.create(customer_username=request.user,restaurant=request.POST['restaurant_name'],number_of_customer=request.POST['number'])
        user = User_info.objects.get(username=request.user)
        user.book = restaurant=request.POST['restaurant_name']
        book.save()
        user.save()
        return render(request,'customer_status.html')