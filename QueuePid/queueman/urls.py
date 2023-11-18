from django.urls import path
from . import views

urlpatterns = [
    path('home/',views.qhome,name='qhome'),
    path('wallet/',views.wallet,name='qwallet'),
    path('profile/',views.profile,name='qprofile'),
    path('profile/edit',views.edit_profile,name='qedit'),
    path('profile/change-password',views.change_password,name='qpassword'),
    path('status',views.status,name='qstatus'),
    path('cancel',views.cancel,name='qcancel')
]