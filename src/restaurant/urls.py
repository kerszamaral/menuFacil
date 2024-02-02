from django.urls import path

from . import views

app_name = 'restaurant'
urlpatterns = [
    path('', views.RestaurantsView.as_view(), name='index'),
    path('<uuid:restaurant_id>/', views.menu, name='detail'),
    path('qrcode/<uuid:tab_id>/', views.get_qrcode, name='qrcode'),
    path('sales/<uuid:restaurant_id>/', views.sales, name='sales'),
    path('search/', views.search, name='search')
]
