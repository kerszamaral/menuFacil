from uuid import UUID
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from django.contrib.messages import get_messages
from restaurant.models import Food, Restaurant

from menuFacil.validation import cart_token_exists, CART_KEY, CART_REDIRECT_URL

from item.models import Item
from .models import Cart

# Create your views here.
def create_cart(request: HttpRequest) -> HttpResponse:
    cart = Cart.objects.create(
        client=request.user if request.user.is_authenticated else None
    )
    request.session[CART_KEY] = cart.id
    return redirect('home')

def add_to_cart(request: HttpRequest, restaurant_id: UUID, food_id: UUID) -> HttpResponse:
    if not cart_token_exists(request.session, request.user):
        return redirect(CART_REDIRECT_URL)

    cart = Cart.objects.get(id=request.session[CART_KEY])

    if cart.restaurant is None:
        cart.restaurant = Restaurant.objects.get(id=restaurant_id)
    elif cart.restaurant.id != restaurant_id:
        messages.error(request, 'Cannot add items from multiple restaurant to cart')
        return redirect('restaurant:detail', args=(restaurant_id,UUID))

    # We use filter and first because if it doesn't find it returns None
    item: Item = cart.item_set.filter(food_id=food_id).first() # type: ignore

    if item:
        item.quantity += 1
    else:
        item = cart.item_set.create( # type: ignore
            food=Food.objects.get(id=food_id),
            order=None
        )

    item.price = item.food.price * item.quantity
    item.save()
    messages.success(request, 'Item added to cart')
    return redirect('restaurant:detail', restaurant_id=restaurant_id)

def increase_quantity(request: HttpRequest, food_id: UUID) -> HttpResponse:
    if not cart_token_exists(request.session, request.user):
        return redirect(CART_REDIRECT_URL)

    cart_item = get_object_or_404(Item, cart_id=request.session[CART_KEY], food_id=food_id)
    cart_item.quantity += 1
    cart_item.price = cart_item.food.price * cart_item.quantity
    cart_item.save()
    messages.success(request, 'Item quantity increased')
    return redirect("cart:cart_detail")

def decrease_quantity(request: HttpRequest, food_id: UUID) -> HttpResponse:
    if not cart_token_exists(request.session, request.user):
        return redirect(CART_REDIRECT_URL)

    cart_item = get_object_or_404(Item, cart_id=request.session[CART_KEY], food_id=food_id)
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
    if not cart_token_exists(request.session, request.user):
        return redirect(CART_REDIRECT_URL)

    cart_item = get_object_or_404(Item, cart_id=request.session[CART_KEY], food_id=food_id)

    cart_item.delete()
    messages.success(request, 'Item removed from cart')
    return redirect("cart:cart_detail")

def cart_detail(request: HttpRequest) -> HttpResponse:
    if not cart_token_exists(request.session, request.user):
        return redirect(CART_REDIRECT_URL)

    cart = Cart.objects.get(id=request.session[CART_KEY])

    context = {
        'cart_items': cart.item_set.all(), # type: ignore
        'total_price': cart.get_total_price(),
        'messages':get_messages(request),
        'cart_length': cart.get_length()
    }

    return render(request, 'cart/cart_detail.html', context)
