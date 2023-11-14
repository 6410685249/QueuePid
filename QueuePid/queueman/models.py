from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Queueman(models.Model):
    username = models.OneToOneField(User,on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=10)
    line_id = models.CharField(max_length=30)
    star = models.IntegerField(default=5)
    credit = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.username}'