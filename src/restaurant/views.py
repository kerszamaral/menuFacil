from typing import Any
from uuid import UUID
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import generic

from cart.models import get_cart_length

from .models import Restaurant

# Create your views here.
class RestaurantsView(generic.ListView):
    template_name = 'restaurant/index.html'
    context_object_name = 'restaurant_list'

    def get_queryset(self) -> QuerySet[Any]:
        return Restaurant.objects.order_by('name')

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        ctx['cart_length'] = get_cart_length(self.request.session, self.request.user)
        return ctx


def menu(request: HttpRequest, restaurant_id: UUID) -> HttpResponse:
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    ctx = {
            'restaurant': restaurant,
            'cart_length': get_cart_length(request.session, request.user)
        }

    return render(request, 'restaurant/detail.html', ctx)
