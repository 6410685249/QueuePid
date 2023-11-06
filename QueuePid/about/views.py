from django.shortcuts import render
from django.http import request
# Create your views here.


def about(request):
    return render(request,'about.html')