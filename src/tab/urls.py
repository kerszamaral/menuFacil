from django.urls import path

from . import views

app_name = 'tab'
urlpatterns = [
    path('', views.details, name='details'),
    path('present/', views.present, name='present'),
    path('history/', views.history, name='history'),
    path('paid/', views.paid, name='paid'),
    path('pay/physical/', views.pay_physical, name='physical'),
    path('pay/online/', views.pay_online, name='online'),
    path('pay/confirm/', views.confirm_payment, name='confirm'),
    path('remove/', views.remove_tab, name='remove'),
    path('get_page/', views.get_tab_page, name='get_page')
]
