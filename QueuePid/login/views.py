from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import RegisterForm
from .models import User_info
def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():

            user = form.save()
            user_info = User_info(
                username=user,
                telephone=form.cleaned_data['telephone'],
                name=form.cleaned_data['name'],
                surname=form.cleaned_data['surname'],
                email=form.cleaned_data['email'],
                type=form.cleaned_data['type'],
            )
            user_info.save()
            # print(form.cleaned_data)
            login(request, user)
            return redirect('about')
    else:
        form = RegisterForm()
    return render(request, 'signup.html', {'form': form})
