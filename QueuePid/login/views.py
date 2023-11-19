from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
# Create your views here.
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import RegisterForm
from .models import User_info
def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        all_emails = User_info.objects.values_list('email', flat=True)
        if form.is_valid():
            if (form.cleaned_data['email'] in list(all_emails)):
                    return render(request, 'signup.html', {'email_unique':'this email has already been used'})
            user = form.save()
            user_info = User_info(
                username=user,
                telephone=form.cleaned_data['telephone'],
                name=form.cleaned_data['name'],
                surname=form.cleaned_data['surname'],
                email=form.cleaned_data['email'],
            )
            user_info.save()
            group = Group.objects.get(name='Customer')
            user.groups.add(group)
            login(request, user)
            return redirect(reverse('login'))
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
            if user.groups.filter(name='Queueman').exists():
                return HttpResponseRedirect(reverse("qhome"))
            else:
                return HttpResponseRedirect(reverse("restaurant_list"))
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

