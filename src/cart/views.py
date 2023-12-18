from uuid import UUID
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.contrib.messages import get_messages

from .models import Cart

# Create your views here.
@login_required
def add_to_cart(request: HttpRequest, restaurant_id: int, food_id: UUID) -> HttpResponse:
    cart_item = Cart.objects.filter(client=request.user, food_id=food_id).first()
    if cart_item:
        cart_item.quantity += 1
        cart_item.price = cart_item.food.price * cart_item.quantity 
        cart_item.save()
        messages.success(request, 'Item added to cart')
    else:
        cart_item = Cart.objects.create(client=request.user, food_id=food_id)
        cart_item.price = cart_item.food.price * cart_item.quantity 
        cart_item.save()
        messages.success(request, 'Item added to cart')
    return HttpResponseRedirect(reverse('restaurant:detail', args=(restaurant_id,)))

@login_required
def increase_quantity(request: HttpRequest, food_id: UUID) -> HttpResponse:
    cart_item = get_object_or_404(Cart, client=request.user, food_id=food_id)
    if cart_item.client == request.user:
        cart_item.quantity += 1
        cart_item.price = cart_item.food.price * cart_item.quantity 
        cart_item.save()
        messages.success(request, 'Item quantity increased')
    return redirect("cart:cart_detail")

@login_required
def decrease_quantity(request: HttpRequest, food_id: UUID) -> HttpResponse:
    cart_item = get_object_or_404(Cart, client=request.user, food_id=food_id)
    if cart_item.client == request.user:
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.price = cart_item.food.price * cart_item.quantity 
            cart_item.save()
            messages.success(request, 'Item quantity decreased')
        else:
            cart_item.delete()
            messages.success(request, 'Item removed from cart')
    return redirect("cart:cart_detail")

@login_required
def remove_from_cart(request: HttpRequest, food_id: UUID) -> HttpResponse:
    cart_item = get_object_or_404(Cart, client=request.user, food_id=food_id)

    if cart_item.client == request.user:
        cart_item.delete()
        messages.success(request, 'Item removed from cart')

    return redirect("cart:cart_detail")

@login_required
def cart_detail(request: HttpRequest) -> HttpResponse:
    cart = Cart.objects.filter(client=request.user)
    total_price = sum(item.quantity * item.food.price for item in cart)

    context = {
        'cart_items': cart,
        'total_price': total_price,
        'messages':get_messages(request),
        'cart_length': sum(item.quantity for item in cart)
    }

    return render(request, 'cart/cart_detail.html', context)
