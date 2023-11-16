from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from .models import Restaurant,Historically
from login.models import User_info
from login.views import logout_view
import re
import smtplib
import random 
from operation.views import booking
def is_valid_email(email):
    # Define the regular expression pattern for a simple email format
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    
    # Use re.match to check if the email matches the pattern
    match = re.match(pattern, email)
    
    # Return True if there is a match, indicating a valid email format
    return bool(match)

def list_restaurant(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    if request.method == 'POST':
        return booking(request,request.POST['restaurant_name'])
    user = User_info.objects.get(username = request.user)


    return render(request, 'customer_home.html', {'form': [(i.name,i.location) for i in Restaurant.objects.all()],'user':user,'book_status':str(user.book)})

def about(request): # render to html
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    return render(request,'customer_about.html')

def wallet(request): # render to html
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    return render(request,'customer_wallet.html')

def account(request): # render to html
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    user = User_info.objects.get(username=request.user)

    return render(request,'customer_account.html',{'user':user})

def edit_page(request,message = "None"):
    # Get the current user's profile (replace with your logic to get the user's profile)
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    user_profile = User_info.objects.get(username=request.user)  
    return render(request,'customer_edit_profile.html',{'user_profile': user_profile,'message':message})

def success_edit(request):
    if request.method == 'POST':
        user_info = User_info.objects.get(username=request.user)
        all_usernames = list(User.objects.values_list('username',flat=True))
        all_emails = list(User_info.objects.values_list('email',flat=True))
        
        all_usernames.remove(user_info.username.username)
        all_emails.remove(user_info.email)

        if (request.POST['username'] in all_usernames):
            return edit_page(request,message='username already use')

        if ((not is_valid_email(request.POST['email'])) or (request.POST['email'] in all_emails)):
            return edit_page(request,message='this email has already been used')

        user_info.username.username = request.POST['username']
        user_info.username.save()
        user_info.name = request.POST['name']
        user_info.surname = request.POST['surname']
        user_info.email = request.POST['email']
        user_info.telephone = request.POST['tele_phone']

        user_info.save()
        return account(request)
    return edit_page(request)

def change_password(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    return render(request,'customer_change_password.html')


def success_password(request):
    if request.method == 'POST':
        new_password = request.POST['password']
        user = request.user
        user.set_password(new_password)
        user.save() 

        return logout_view(request)
    return change_password(request)


def history(request): # render to html
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    return render(request,'customer_history.html',{'history': [i for i in Historically.objects.filter(username=request.user)]})

def verify_gmail(request, message="None"):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    user = User_info.objects.get(username=request.user)

    # Check if verify_num is already stored in the session
    if 'verify_num' in request.session:
        verify_num = request.session['verify_num']
    else:
        # Generate a new verify_num if not already in the session
        verify_num = ''.join([str(random.randint(0, 9)) for i in range(6)])
        request.session['verify_num'] = verify_num

        # Send the verification email
        smtp_object = smtplib.SMTP('smtp.gmail.com', 587)
        smtp_object.ehlo()
        smtp_object.starttls()
        email = 'queuepidcorp@gmail.com'
        password = 'jvqk fwso vgkq jlvp'
        smtp_object.login(email, password)
        msg = 'Subject: ' + 'verify number' + '\n' + verify_num
        smtp_object.sendmail(email, user.email, msg)
        smtp_object.quit()

    if request.method == 'POST':
        entered_verify_num = str(request.POST.get('verify_number', ''))

        if entered_verify_num == verify_num:
            user.verify_gmail = True
            user.save()
            del request.session['verify_num']  # Remove stored verify_num from session
            return account(request)
        else:
            return verify_gmail(request, message="verify_number mismatch")

    return render(request, 'customer_verifygmail.html', {'message': message})


