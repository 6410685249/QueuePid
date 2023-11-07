from django.urls import path
from . import views

urlpatterns = [
    path('restaurant_list',views.list_restaurant,name='restaurant_list'),
    path('restaurant_list/history',views.history,name='go_to_history_page'),
    
    path('restaurant_list/history_back_to_home',views.in_history_back_to_home,name='history_back_to_home'),
    path('restaurant_list/about',views.go_to_about_page,name='go_to_about_page'),
    path('restaurant_list/go_to_about_page',views.about,name='about'),
    path('restaurant_list/in_about_back_to_home',views.in_about_back_to_home,name='in_about_back_to_home'),

    path('restaurant_list/wallet',views.go_to_wallet_page,name='go_to_wallet_page'),
    path('restaurant_list/go_to_wallet_page',views.wallet,name='wallet'),
    path('restaurant_list/in_wallet_back_to_home',views.in_wallet_back_to_home,name='in_wallet_back_to_home'),

    path('restaurant_list/account',views.go_to_account_page,name='go_to_account_page'),
    path('restaurant_list/go_to_wallet_page',views.account,name='account'),
    path('restaurant_list/in_account_back_to_home',views.in_account_back_to_home,name='in_account_back_to_home'),

]