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
    path('restaurant_list/account',views.go_to_account_page,name='go_to_account_page'),

    path('restaurant_list/account/edit_profile',views.go_to_edit_profile_page,name='go_to_edit_profile_page'),
    path('restaurant_list/account/in_edit_back_account',views.in_edit_back_account,name='in_edit_back_account'),
    path('restaurant_list/account/in_success_edit_back_account',views.in_success_edit_back_account,name='in_success_edit_back_account'),

    path('restaurant_list/account/go_to_change_password_page',views.go_to_change_password_page,name='go_to_change_password_page'),
    path('restaurant_list/account/in_change_password_back_to_account',views.in_change_password_back_to_account,name='in_change_password_back_to_account'),
    path('restaurant_list/account/change_password',views.change_password,name='change_password'),
    path('restaurant_list/account/in_complete_change_password_back_to_account',views.complete_password,name='in_complete_change_password_back_to_account'),


]