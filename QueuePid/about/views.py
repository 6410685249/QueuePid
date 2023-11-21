from django.shortcuts import render
from django.http import request,HttpResponse
# Create your views here.
from django.db import models
from ipware import get_client_ip
from ip2geotools.databases.noncommercial import DbIpCity

def more_about_us(request):
    return render(request,'about.html')

def queuepid(request):
    return render(request, 'queuepid.html')

def about_queuepid(request):
    return render(request, 'about_queuepid.html')

def get_client_ip_view(request):
    # Get the client's IP address using ipware's get_client_ip function
    client_ip, is_routable = get_client_ip(request)
    
    country = response.latitude
    if client_ip is None:
        # Unable to get the client's IP address
        result = "Unable to determine client's IP address"
    else:
        result = f'Client IP Address: {client_ip}'

    try :
        response = DbIpCity.get(client_ip,api_key=True)
        la = response.latitude
        long = response.longitude
    except:
        la = "None la"
        long = "None long" 
    return render(request, 'test.html', {'result': result,'latitude':la,'longtitude':long})