from django.urls import path
from . import views

urlpatterns = [
    path('customer_home',views.list_restaurant,name='restaurant_list'),
 
    path('customer_home/about',views.go_to_about_page,name='about_page'),
    path('customer_home/go_to_about_page',views.about,name='about'),
    path('customer_home/acount_back',views.acount_back,name='acount_back'),

    path('customer_home/wallet',views.wallet_page,name='wallet_page'),
    path('customer_home/account',views.account_page,name='account_page'),

    path('customer_home/account/edit_page',views.edit_page,name='edit_page'),
    path('customer_home/account/success_edit',views.success_edit,name='success_edit'),
    path('customer_home/account/change_password',views.change_password,name='change_password'),
    path('customer_home/account/success_password',views.success_password,name='success_password'),

    path('customer_home/history',views.history,name='history'),

]