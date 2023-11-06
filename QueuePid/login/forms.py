from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation

from .models import User_info


class RegisterForm(UserCreationForm):
    name = forms.CharField(max_length=30, required=True)
    surname = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, required=True)
    telephone = forms.CharField(max_length=30, required=True)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Remove the default help texts for the password fields
        for field_name in ['password1', 'password2']:
            self.fields[field_name].help_text = None
        self.fields['username'].help_text = None
    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        password_validation.validate_password(password1, self.user)
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError("The two password fields didn't match.")
        return password2

