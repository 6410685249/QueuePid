from django.db import models
from django.contrib.auth.models import User
from customers.models import Restaurant
# Create your models here.
class User_info(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)    
    telephone = models.CharField(max_length=10)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    credit = models.PositiveIntegerField(default=0)
    verify_gmail = models.BooleanField(default=False)
    book = models.CharField(max_length=30, null=True, blank=True,default="None")

    def __str__(self) -> str:
        return f"{self.username} {self.name} {self.surname} {self.email} {self.credit}"