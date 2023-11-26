from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from queueman.models import Queueman
# Create your views here.
def more_about_us(request):
    return render(request,'about.html')

def queuepid(request):
    return render(request, 'queuepid.html')

def about_queuepid(request):
    return render(request, 'about_queuepid.html')
