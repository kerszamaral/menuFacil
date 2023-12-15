from django.urls import path

from . import views

app_name = 'restaurant'
urlpatterns = [
    path('', views.RestaurantsView.as_view(), name='index'),
    path('<int:pk>/', views.RestaurantView.as_view(), name='detail'),
]
