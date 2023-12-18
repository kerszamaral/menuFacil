from uuid import UUID
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.messages import get_messages

from cart.models import Cart
from .models import Order

# Create your views here.
@login_required(login_url="/account/login/")
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
    ctx = {
            'order': order, 'restaurant': restaurant, 
            'messages':get_messages(request), 
            'cart_length': Cart.get_cart_length(request.user)
        }
    return render(request, 'order/validate.html', ctx)

@login_required(login_url="/account/login/")
def confirm_order(request: HttpRequest, order_id: UUID) -> HttpResponse:
    # if not request.user.is_staff:
        # return HttpResponse('Unauthorized', status=401)
        
    order = get_object_or_404(Order, id=order_id)
    order.status = Order.StatusType.MADE
    order.save()
    return redirect('order:pay_order', order_id=order.id)

@login_required(login_url="/account/login/")
def list_orders(request: HttpRequest) -> HttpResponse:
    orders = Order.objects.filter(client=request.user)
    orders = orders.order_by('-created_at')
    ctx = {
            'orders': orders,
            "open": Order.StatusType.OPEN,
            'messages':get_messages(request),
            'cart_length': Cart.get_cart_length(request.user)
        }
    
    return render(request, 'order/list.html', ctx)

@login_required(login_url="/account/login/")
def details_order(request: HttpRequest, order_id: UUID) -> HttpResponse:
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order/details.html', {'order': order, 'messages':get_messages(request), 'cart_length': Cart.get_cart_length(request.user)})
    
@login_required(login_url="/account/login/")
def reopen_confirm_order(request: HttpRequest, order_id: UUID) -> HttpResponse:
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order/validate.html', {'order': order, 'messages':get_messages(request), 'cart_length': Cart.get_cart_length(request.user)})

@login_required(login_url="/account/login/")
def cancel_order(request: HttpRequest, order_id: UUID) -> HttpResponse:
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order/validate.html', {'order': order, 'restaurant': order.restaurant, 'cancel': True, 'messages':get_messages(request), 'cart_length': Cart.get_cart_length(request.user)})

@login_required(login_url="/account/login/")
def cancel_order_confirm(request: HttpRequest, order_id: UUID) -> HttpResponse:
    order = get_object_or_404(Order, id=order_id)
    order.pending_cancellation = True
    order.save()
    return redirect('order:list_orders')

@login_required(login_url="/account/login/")
def pay_order(request: HttpRequest, order_id: UUID) -> HttpResponse:
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order/validate.html', {'order': order, 'restaurant': order.restaurant, 'pay': True, 'messages':get_messages(request), 'cart_length': Cart.get_cart_length(request.user)})

@login_required(login_url="/account/login/")
def payed_order(request: HttpRequest, order_id: UUID) -> HttpResponse:
    order = get_object_or_404(Order, id=order_id)
    order.payed = True
    order.save()
    return redirect('order:list_orders')