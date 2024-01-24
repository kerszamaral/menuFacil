from django.urls import path

from . import views

app_name = 'tab'
urlpatterns = [
    path('', views.list_orders_in_tab, name='index'),
]
