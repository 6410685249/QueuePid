from django.shortcuts import render
from django.http import request,HttpResponse
# Create your views here.
from django.db import models
from ipware import get_client_ip
from ip2geotools.databases.noncommercial import DbIpCity
from customers.models import Restaurant
def more_about_us(request):
    return render(request,'about.html')

def queuepid(request):
    return render(request, 'queuepid.html')

def about_queuepid(request):
    return render(request, 'about_queuepid.html')
