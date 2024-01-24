from django.urls import path

from . import views

app_name = 'cart'
urlpatterns = [
    path('create', views.create_cart, name='create'),
    path("add/<uuid:restaurant_id>/<uuid:food_id>/", views.add_to_cart, name="add_to_cart"),
    path("inc_quantity/<uuid:food_id>/", views.increase_quantity, name="increase_quantity"),
    path("dec_quantity/<uuid:food_id>/", views.decrease_quantity, name="decrease_quantity"),
    path("remove/<uuid:food_id>/", views.remove_from_cart, name="remove_from_cart"),
    path('', views.cart_detail, name="cart_detail"),
]
