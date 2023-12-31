from django.db import models
from django.contrib.auth.models import User
from location_field.models.plain import PlainLocationField

# Create your models here.
class Queueman(models.Model):
    username = models.OneToOneField(User,on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=10)
    line_id = models.CharField(max_length=30)
    star = models.FloatField(default=5)
    credit = models.PositiveIntegerField(default=0)
    is_have_queue = models.BooleanField(default=False)
    upload =  models.PositiveIntegerField(default=0)
    location_address = PlainLocationField(zoom=7, null=True,default=None,blank=True)
    
    def __str__(self):
        return f'{self.username}'