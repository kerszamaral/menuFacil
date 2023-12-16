from django.urls import path

from . import views

app_name = 'order'
urlpatterns = [
    path('create/', views.create_order, name='create_order'),
    path('confirm/<uuid:order_id>/', views.confirm_order, name='confirm_order'),
    path('list/', views.list_orders, name='list_orders'),
    path('details/<uuid:order_id>/', views.details_order, name='details_order'),
    path('reopen/<uuid:order_id>/', views.reopen_confirm_order, name='reopen_confirm_order')
]
