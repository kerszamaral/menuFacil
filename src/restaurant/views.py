from typing import Any
from uuid import UUID
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import generic

from .models import Restaurant

# Create your views here.
class RestaurantsView(generic.ListView):
    template_name = 'restaurant/index.html'
    context_object_name = 'restaurant_list'

    def get_queryset(self) -> QuerySet[Any]:
        return Restaurant.objects.order_by('name')



def menu(request: HttpRequest, restaurant_id: UUID) -> HttpResponse:
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)

    return render(request, 'restaurant/detail.html', {'restaurant': restaurant})
