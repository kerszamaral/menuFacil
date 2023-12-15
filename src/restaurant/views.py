from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import generic

from .models import Restaurant

# Create your views here.
class RestaurantsView(generic.ListView):
    template_name = 'restaurant/index.html'
    context_object_name = 'restaurant_list'
    
    def get_queryset(self) -> QuerySet[Any]:
        return Restaurant.objects.order_by('name')
    
    
class RestaurantView(generic.DetailView):
    model = Restaurant
    template_name = 'restaurant/detail.html'
    
    # def get_queryset(self) -> QuerySet[Any]:
    #     return Restaurant.objects.all()