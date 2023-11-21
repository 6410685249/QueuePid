from django.urls import path
from . import views

urlpatterns = [
    path('',views.queuepid,name='queuepid'),
    path('about/',views.about_queuepid,name='about_queuepid'),
    path('more/',views.more_about_us, name="more_about_us"),
    path('ip_test',views.get_client_ip_view, name="get_client_ip_view"),
    path('ip_js',views.ip_js, name="ip_js"),
]