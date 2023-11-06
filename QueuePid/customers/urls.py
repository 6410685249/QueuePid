from django.urls import path
from . import views

urlpatterns = [
    path('home',views.list_restaurant,name='home'),

]