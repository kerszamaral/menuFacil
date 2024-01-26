from django.urls import path

from . import views

app_name = 'tab'
urlpatterns = [
    path('', views.details, name='details'),
    path('present/', views.present, name='present'),
]
