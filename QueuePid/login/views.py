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
    # print('In signup')
    if request.method == 'POST':
        # print("in post")
        form = RegisterForm(request.POST)
        if form.is_valid():
            # print('form valid')
            user = form.save()
            print(form.cleaned_data)
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
            return redirect(reverse('restaurant_list'))
    else:
        form = RegisterForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        queueman_group = Group.objects.get(name="Queueman").user_set.all()
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user in queueman_group:
                login(request, user)
                return HttpResponseRedirect(reverse("qhome"))
            else:
                login(request, user)
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

