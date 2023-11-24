from django.db import models
from django.contrib.auth.models import User
from customers.models import Restaurant
from django.utils.html import mark_safe

# Create your models here.
class User_info(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)    
    telephone = models.CharField(max_length=10)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    credit = models.IntegerField(default=0)
    verify_gmail = models.BooleanField(default=False)
    book = models.CharField(max_length=30, null=True, blank=True,default=None)
    upload =  models.ImageField(upload_to='uploads/', null=True,default=None, blank=True)
    credit_topUp = models.IntegerField(default=0)
    message_from_admin = models.CharField(max_length=100,default="",null=True, blank=True)
    def __str__(self) -> str:
        return f"{self.username} {self.name} {self.surname} {self.email} {self.credit}"
