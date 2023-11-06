from django.urls import path, include
from . import views

urlpatterns = [
    path('signup',view=views.signup,name='signup')

]