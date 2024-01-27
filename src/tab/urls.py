from django.urls import path

from . import views

app_name = 'tab'
urlpatterns = [
    path('', views.details, name='details'),
    path('present/', views.present, name='present'),
    path('history/', views.history, name='history'),
    path('payed/', views.payed, name='payed'),
    path('pay/physical/', views.pay_physical, name='physical'),
    path('pay/online/', views.pay_online, name='online'),
]
