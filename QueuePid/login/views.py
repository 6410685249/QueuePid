from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
# Create your views here.
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import RegisterForm
from .models import User_info
def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
       # print(form)
        if form.is_valid():

            user = form.save()
            user_info = User_info(
                username=user,
                telephone=form.cleaned_data['telephone'],
                name=form.cleaned_data['name'],
                surname=form.cleaned_data['surname'],
                email=form.cleaned_data['email'],
            )
            user_info.save()
            # print(form.cleaned_data)
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("home"))
        else:
            return render(request, 'login.html', {
                'message': 'Invalid credentials!'
            })
    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return render(request, 'login.html', {
        'message': 'Logged out'
    })

