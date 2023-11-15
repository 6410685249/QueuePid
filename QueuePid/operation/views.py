from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
# Create your views here.
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .models import *
# Create your views here.
# Create your views here.
def booking(request, restaurant_name):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    return render(request, 'customer_booking.html',{'restaurant':restaurant_name})

def get_number_of_customer(request):

    if request.method == 'POST':
        print('IN booking')
        print(request.POST)
        book = Booking.objects.create(customer_username=request.user,restaurant=request.POST['restaurant_name'],number_of_customer=request.POST['number'])
        book.save()
        return render(request,'customer_status.html')