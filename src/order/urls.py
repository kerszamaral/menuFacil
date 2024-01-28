from django.urls import path

from . import views

app_name = 'order'
urlpatterns = [
    path('create/', views.create, name='create'),
    path('cancel/', views.cancel, name='cancel'),
]
