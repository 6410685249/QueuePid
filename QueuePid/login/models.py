from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class User_info(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)    
    telephone = models.CharField(max_length=10)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    type = models.CharField(max_length = 10,default='customer')
    credit = models.PositiveIntegerField(default='customer')
    def __str__(self) -> str:
        return f'{self.name} {self.surname} {self.telephone} {self.email}'