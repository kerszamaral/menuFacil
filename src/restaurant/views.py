from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.views import generic
from django.urls import reverse

from .models import Restaurant, Food

# Create your views here.
class RestaurantsView(generic.ListView):
    template_name = 'restaurant/index.html'
    context_object_name = 'restaurant_list'

    def get_queryset(self) -> QuerySet[Any]:
        return Restaurant.objects.order_by('name')


def menu(request: HttpRequest, restaurant_id: int) -> HttpResponse:
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    
    if request.method == 'POST' and request.user.is_authenticated:
        food_id = request.POST['food_id']
        food = get_object_or_404(Food, pk=food_id)
        messages.success(request, f"{food.name} added to cart.")
        return redirect('cart:add_to_cart', restaurant_id=restaurant_id, food_id=food_id)
    
    return render(request, 'restaurant/detail.html', {'restaurant': restaurant})
        