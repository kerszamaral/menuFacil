from django.urls import path

from . import views

app_name = 'cart'
urlpatterns = [
    path('create/', views.create, name='create'),
    path("add/<uuid:restaurant_id>/<uuid:food_id>/", views.add, name="add"),
    path("inc_quantity/<uuid:food_id>/", views.increase_quantity, name="increase_quantity"),
    path("dec_quantity/<uuid:food_id>/", views.decrease_quantity, name="decrease_quantity"),
    path("remove/<uuid:food_id>/", views.remove, name="remove"),
    path('', views.details, name="details"),
]
