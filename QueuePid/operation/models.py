from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from login.models import User_info 
from django.contrib.auth.models import User

# Create your models here.
class Review(models.Model):

    queueman_username = models.CharField(max_length=30)
    customer_username = models.CharField(max_length=30)
    comment = models.CharField(max_length=500)
    star = models.DecimalField(
        max_digits=3,  # Adjust this based on your needs
        decimal_places=2,  # Adjust this based on your needs
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ])
    type = models.ImageField(upload_to='uploads/', null=True,default=None)

    def __str__(self):
        return f"{self.queueman_username} {self.customer_username} {self.comment} {self.star}"
    
class Booking(models.Model):
    customer_username = models.OneToOneField(User,on_delete=models.CASCADE)
    restaurant = models.CharField(max_length=30)
    number_of_customer = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.customer_username} {self.restaurant} {self.number_of_customer} "

class Operation(models.Model):

    customer_username = models.CharField(max_length=30)
    restaurant = models.CharField(max_length=30)
    cost = models.CharField(max_length=30)
    queueMan_username = models.CharField(max_length=30)
    date = models.DateTimeField(null=True)
    number_Queue = models.IntegerField(null=True)
    number_of_customer = models.CharField(max_length=30)
    status = models.IntegerField(default=-1)
    cancel_by_queueman = models.BooleanField(default=False)
    cancel_by_user = models.BooleanField(default=False)
    update_status = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.customer_username} {self.restaurant} {self.queueMan_username} "

