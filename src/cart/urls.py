from django.urls import path

from . import views

app_name = 'cart'
urlpatterns = [
    path("add/", views.add, name="add"),
    path("inc/", views.increase_quantity, name="inc"),
    path("dec/", views.decrease_quantity, name="dec"),
    path("remove/", views.remove, name="remove"),
    path('', views.details, name="details"),
]
