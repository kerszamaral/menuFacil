from django.urls import path

from . import views

app_name = 'order'
urlpatterns = [
    path('create/', views.create_order, name='create_order'),
    path('cancel/<uuid:order_id>/', views.cancel_order, name='cancel_order'),
]
