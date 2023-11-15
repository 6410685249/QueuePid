from django.urls import path
from . import views

urlpatterns = [
    path('customer_home',views.list_restaurant,name='restaurant_list'),
    path('customer_home/about',views.about,name='about'),
    path('customer_home/wallet',views.wallet,name='wallet'),
    path('customer_home/account',views.account,name='account'),
    path('customer_home/account/edit_page',views.edit_page,name='edit_page'),
    path('customer_home/account/success_edit',views.success_edit,name='success_edit'),
    path('customer_home/account/change_password',views.change_password,name='change_password'),
    path('customer_home/account/success_password',views.success_password,name='success_password'),
    path('customer_home/history',views.history,name='history'),
    path('customer_home/verify_gmail',views.verify_gmail,name='verify_gmail'),

]