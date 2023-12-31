from django.urls import path

from . import views

app_name = 'restaurant'
urlpatterns = [
    path('', views.RestaurantsView.as_view(), name='index'),
    path('<int:restaurant_id>/', views.menu, name='detail'),
]
