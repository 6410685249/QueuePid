from django.urls import path
from . import views
urlpatterns = [
    path('customer_home/booking',views.booking,name='booking'),
    path('customer_home/get_number_of_customer',views.get_number_of_customer,name='get_number_of_customer'),
    path('customer_home/customer_status',views.customer_status,name='customer_status'),
    path('customer_home/customer_payment',views.customer_payment,name='customer_payment'),
    path('customer_complete',views.customer_complete,name='customer_complete'),
    path('customer_review',views.customer_review,name='customer_review'),
    path('customer_report',views.customer_report,name='customer_report'),
    path('customer_cancel',views.customer_cancel,name='customer_cancel'),

]