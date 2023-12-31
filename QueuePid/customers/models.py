from django.db import models
from location_field.models.plain import PlainLocationField
# Create your models here.
class Restaurant(models.Model):

    name = models.CharField(max_length=30,unique=True,primary_key=True)
    phone_number = models.CharField(max_length=30,unique=True)
    line_id = models.CharField(max_length=30,unique=True)
    location = models.CharField(max_length=30)
    upload = models.ImageField(upload_to='uploads/', null=True,default=None,blank=True)
    location_address = PlainLocationField(zoom=7, null=True,default=None,blank=True)

    def __str__(self) -> str:
        return f"{self.name} {self.phone_number} {self.line_id} {self.location}"
    
class Historically(models.Model):

    username = models.CharField(max_length=30)
    restaurant = models.CharField(max_length=30)
    cost = models.CharField(max_length=30)
    queeuManName = models.CharField(max_length=30)
    date = models.DateField(max_length=30)
    phone_number_QueueMan = models.CharField(max_length=30)
    phone_number_customer = models.CharField(max_length=30)

    def __str__(self) -> str:
        return f"{self.username} {self.restaurant} {self.phone_number_QueueMan} {self.phone_number_customer}"