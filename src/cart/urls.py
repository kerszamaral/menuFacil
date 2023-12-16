from django.urls import path

from . import views

app_name = 'cart'
urlpatterns = [
    path('', views.cart_detail, name="cart_detail"),
    path("add/<int:restaurant_id>/<uuid:food_id>/", views.add_to_cart, name="add_to_cart"),
    path("remove/<uuid:food_id>/", views.remove_from_cart, name="remove_from_cart"),
]
