from django.urls import path
from . import views
urlpatterns = [
    path('customer_home/booking',views.booking,name='booking'),
    path('customer_home/get_number_of_customer',views.get_number_of_customer,name='get_number_of_customer'),
    
]