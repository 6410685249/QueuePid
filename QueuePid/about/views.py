from django.shortcuts import render
# Create your views here.
def more_about_us(request):
    return render(request,'about.html')

def queuepid(request):
    return render(request, 'queuepid.html')

def about_queuepid(request):
    return render(request, 'about_queuepid.html')
