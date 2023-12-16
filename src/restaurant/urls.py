from django.urls import path

from . import views

app_name = 'restaurant'
urlpatterns = [
    path('', views.RestaurantsView.as_view(), name='index'),
    path('<int:pk>/', views.RestaurantView.as_view(), name='detail'),
    path('<int:restaurant_id>/<int:menu_id>/<int:food_id>/', views.cart, name='cart'),
    path('<int:restaurant_id>/close/', views.close_cart, name='close_cart'),
]
