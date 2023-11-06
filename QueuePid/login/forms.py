from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User_info


class RegisterForm(UserCreationForm):
    name = forms.CharField(max_length=30, required=True, help_text='Required.')
    surname = forms.CharField(max_length=30, required=True, help_text='Required.')
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')
    telephone = forms.CharField(max_length=30, required=True, help_text='Required.')
    type = forms.CharField(max_length = 10,help_text='Customer')


