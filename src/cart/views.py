from uuid import UUID
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.messages import get_messages
from restaurant.models import Food, Restaurant

from validation import cart_token_exists, CART_KEY, CART_REDIRECT_URL

from .models import Item, Cart

# Create your views here.
def add_to_cart(request: HttpRequest, restaurant_id: UUID, food_id: UUID) -> HttpResponse:
    if not cart_token_exists(request):
        return redirect(CART_REDIRECT_URL)

    cart_token = request.session[CART_KEY]

    cart_item = Item.objects.get(cart_id=cart_token, food_id=food_id)

    if cart_item:
        cart_item.quantity += 1
    else:
        cart = Cart.objects.get(id=cart_token)
        food =  Food.objects.get(id=food_id)
        cart_item = cart.item_set.create(
            food=food
        )
 
    cart_item.price = cart_item.food.price * cart_item.quantity
    cart_item.save()
    messages.success(request, 'Item added to cart')
    return HttpResponseRedirect(reverse('restaurant:detail', args=(restaurant_id,UUID)))

def increase_quantity(request: HttpRequest, food_id: UUID) -> HttpResponse:
    if not cart_token_exists(request):
        return redirect(CART_REDIRECT_URL)

    cart_token = request.session[CART_KEY]
    cart_item = get_object_or_404(Item, cart_id=cart_token, food_id=food_id)
    cart_item.quantity += 1
    cart_item.price = cart_item.food.price * cart_item.quantity
    cart_item.save()
    messages.success(request, 'Item quantity increased')
    return redirect("cart:cart_detail")

def decrease_quantity(request: HttpRequest, food_id: UUID) -> HttpResponse:
    if not cart_token_exists(request):
        return redirect(CART_REDIRECT_URL)

    cart_token = request.session[CART_KEY]

    cart_item = get_object_or_404(Item, cart_id=cart_token, food_id=food_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.price = cart_item.food.price * cart_item.quantity
        cart_item.save()
        messages.success(request, 'Item quantity decreased')
    else:
        cart_item.delete()
        messages.success(request, 'Item removed from cart')
    return redirect("cart:cart_detail")

def remove_from_cart(request: HttpRequest, food_id: UUID) -> HttpResponse:
    if not cart_token_exists(request):
        return redirect(CART_REDIRECT_URL)

    cart_token = request.session[CART_KEY]
    cart_item = get_object_or_404(Item, cart_id=cart_token, food_id=food_id)

    cart_item.delete()
    messages.success(request, 'Item removed from cart')

    return redirect("cart:cart_detail")

def cart_detail(request: HttpRequest) -> HttpResponse:
    if not cart_token_exists(request):
        return redirect(CART_REDIRECT_URL)

    cart_token = request.session[CART_KEY]
    cart_items = Item.objects.filter(cart_id=cart_token)
    total_price = sum(item.price for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'messages':get_messages(request),
        'cart_length': sum(item.quantity for item in cart_items)
    }

    return render(request, 'cart/cart_detail.html', context)
