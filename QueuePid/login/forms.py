from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation
from django.core.validators import EmailValidator

from .models import User_info


class RegisterForm(UserCreationForm):
    name = forms.CharField(max_length=30, required=True)
    surname = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(
        max_length=254,
        required=True,
        validators=[EmailValidator(message='Enter a valid email address.')]
    )    
    telephone = forms.CharField(max_length=30, required=True)
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    #     # Remove the default help texts for the password fields
    #     for field_name in ['password1', 'password2']:
    #         self.fields[field_name].help_text = None
    #     self.fields['username'].help_text = None


