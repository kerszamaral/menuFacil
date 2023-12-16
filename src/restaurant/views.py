from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.urls import reverse

from .models import Restaurant, Menu, Food
from client.models import Order, Item

# Create your views here.
class RestaurantsView(generic.ListView):
    template_name = 'restaurant/index.html'
    context_object_name = 'restaurant_list'
    
    def get_queryset(self) -> QuerySet[Any]:
        return Restaurant.objects.order_by('name')
    
    
class RestaurantView(generic.DetailView):
    model = Restaurant
    template_name = 'restaurant/detail.html'
    
def close_cart(request: HttpRequest, restaurant_id: int) -> HttpResponse:
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    if request.user.is_anonymous:
        return HttpResponseRedirect(reverse('client:login'))
    if not request.user.order_set.filter(restaurant=restaurant, status=Order.StatusType.OPEN).exists():
        print("Error: Cart is not open.")
        return render(request, 'restaurant/detail.html', {
                'restaurant': restaurant,
                'error_message': "Your cart is not open.",
            })
    order = request.user.order_set.get(restaurant=restaurant, status=Order.StatusType.OPEN)
    order.status = Order.StatusType.PENDING
    order.save()
    print(order.item_set.all())
    return HttpResponseRedirect(reverse('client:orders'))
        
    
def cart(request: HttpRequest, restaurant_id: int, menu_id: int, food_id: int) -> HttpResponse:
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    try:
        selected_menu = restaurant.menu_set.get(pk=menu_id)
    except (KeyError, Menu.DoesNotExist):
        return render(request, 'restaurant/detail.html', {
            'restaurant': restaurant,
            'error_message': "Menu does not exist.",
        })
    else:
        try:
            selected_food = selected_menu.food_set.get(pk=food_id)
        except (KeyError, Food.DoesNotExist):
            return render(request, 'restaurant/detail.html', {
                'restaurant': restaurant,
                'selected_menu': selected_menu,
                'error_message': "Food does not exist.",
            })
        else:
            if request.user.is_anonymous:
                return HttpResponseRedirect(reverse('client:login'))
            
            if request.user.order_set.filter(restaurant=restaurant, status=Order.StatusType.OPEN).exists():
                order = request.user.order_set.get(restaurant=restaurant, status=Order.StatusType.OPEN)
                order.total_price += selected_food.price
                
                if order.item_set.filter(food=selected_food).exists():
                    i = order.item_set.get(food=selected_food)
                    i.quantity += 1
                    i.save()
                else:
                    i = order.item_set.create(
                        food=selected_food,
                        quantity=1,
                    )
            else:
                order = Order(
                    client=request.user,
                    restaurant=restaurant,
                    total_price=selected_food.price,
                    status=Order.StatusType.OPEN,
                )
                order.save()
                i = order.item_set.create(
                    food=selected_food,
                    quantity=1,
                )
            order.save()
            for item in order.item_set.all():
                print(item)
            return HttpResponseRedirect(reverse('restaurant:detail', args=(restaurant.id,)))