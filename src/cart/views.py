from django.shortcuts import get_object_or_404, render
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from restaurant.models import Food, Restaurant

from menuFacil.validation import post_contains_keys

from item.models import Item
from .models import Cart, CART_KEY

# Create your views here.
@require_POST
def add(request: HttpRequest) -> HttpResponse:
    if not post_contains_keys(request.POST, ['food', 'restaurant']):
        return JsonResponse({"success": False}, status=400)

    if request.user.is_authenticated:
        request.session[CART_KEY] = str(request.user.cart.id) # type: ignore

    (cart, created)= Cart.objects.get_or_create(id=request.session.get(CART_KEY, None),
                        defaults={'client': request.user if request.user.is_authenticated else None}
                    )
    if created:
        request.session[CART_KEY] = str(cart.id)

    if cart.restaurant is None:
        cart.restaurant = Restaurant.objects.get(id=request.POST['restaurant'])
    elif str(cart.restaurant.id) != request.POST['restaurant']:
        messages.error(request, 'Cannot add items from multiple restaurant to cart')
        return JsonResponse({"success": False}, status=406)

    cart.save()

    # We use filter and first because if it doesn't find it returns None
    item: Item = cart.item_set.filter(food_id=request.POST['food']).first() # type: ignore

    if item is None:
        food = get_object_or_404(Food, id=request.POST['food'])
        item = cart.item_set.create( # type: ignore
            food=food,
            order=None,
            price=food.price,
        )
    else:
        item.quantity += 1
        item.save()

    messages.success(request, 'Item added to cart')
    return JsonResponse({"success": True}, status=200)

@require_POST
def increase_quantity(request: HttpRequest) -> HttpResponse:
    if not post_contains_keys(request.POST, ['item']):
        return JsonResponse({"success": False}, status=400)

    item = get_object_or_404(Item, id=request.POST['item'])
    item.quantity += 1
    item.save()
    messages.success(request, 'Item quantity increased')
    return JsonResponse({"success": True}, status=200)

@require_POST
def decrease_quantity(request: HttpRequest) -> HttpResponse:
    if not post_contains_keys(request.POST, ['item']):
        return JsonResponse({"success": False}, status=400)

    item = get_object_or_404(Item, id=request.POST['item'])
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
        messages.success(request, 'Item quantity decreased')
    else:
        item.delete()
        messages.success(request, 'Item removed from cart')
    return JsonResponse({"success": True}, status=200)

@require_POST
def remove(request: HttpRequest) -> HttpResponse:
    if not post_contains_keys(request.POST, ['item']):
        return JsonResponse({"success": False}, status=400)

    item = get_object_or_404(Item, id=request.POST['item'])

    item.delete()
    messages.success(request, 'Item removed from cart')
    return JsonResponse({"success": True}, status=200)

def details(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        request.session[CART_KEY] = str(request.user.cart.id) # type: ignore

    (cart, created)= Cart.objects.get_or_create(id=request.session.get(CART_KEY, None),
                        defaults={'client': request.user if request.user.is_authenticated else None}
                    )
    if created:
        request.session[CART_KEY] = str(cart.id)

    return render(request, 'cart/details.html', {'cart': cart})
