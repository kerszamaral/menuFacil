from uuid import UUID
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from cart.models import Cart
from .models import Order

# Create your views here.
@login_required
def create_order(request: HttpRequest) -> HttpResponse:
    cart = Cart.objects.filter(client=request.user)
    restaurant = cart.first().food.menu.restaurant
    order = Order.objects.create(
        client=request.user,
        restaurant=restaurant,
        total_price=sum(item.quantity * item.food.price for item in cart),
        status = Order.StatusType.OPEN,
    )
    order.save()
    for item in cart:
        order.item_set.create(
            food=item.food,
            quantity=item.quantity,
            price=item.price,
        )
    cart.delete()
    return render(request, 'order/validate.html', {'order': order, 'restaurant': restaurant})

@login_required
def confirm_order(request: HttpRequest, order_id: UUID) -> HttpResponse:
    # if not request.user.is_staff:
        # return HttpResponse('Unauthorized', status=401)
        
    order = get_object_or_404(Order, id=order_id)
    order.status = Order.StatusType.MADE
    order.save()
    return redirect('order:list_orders')

@login_required
def list_orders(request: HttpRequest) -> HttpResponse:
    orders = Order.objects.filter(client=request.user)
    orders = orders.order_by('-created_at')
    
    return render(request, 'order/list.html', {'orders': orders, "open": Order.StatusType.OPEN})

@login_required
def details_order(request: HttpRequest, order_id: UUID) -> HttpResponse:
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order/details.html', {'order': order})
    
@login_required
def reopen_confirm_order(request: HttpRequest, order_id: UUID) -> HttpResponse:
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order/validate.html', {'order': order})