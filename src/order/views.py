from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages

from item.models import Item
from cart.models import Cart
from tab.models import Tab
from menuFacil.validation import contains, valid_uuid
from .models import Order

# Create your views here.
@require_POST
def create(request: HttpRequest) -> HttpResponse:
    if not contains(request.POST, ['cart', 'tab']):
        return JsonResponse({"success": False}, status=400)

    cart = get_object_or_404(Cart, id=request.POST['cart'])
    if cart.restaurant is None:
        return JsonResponse({"success": False}, status=404)

    if not valid_uuid(request.POST['tab']):
        return JsonResponse({"success": False}, status=412)
    try:
        tab = Tab.objects.get(id=request.POST['tab'])
    except KeyError:
        return JsonResponse({"success": False}, status=412)
    
    if tab.restaurant is None:
        tab.restaurant = cart.restaurant
        tab.save()
    elif tab.restaurant.id != cart.restaurant.id:
        messages.error(request, 'Cannot order from multiple restaurant to tab')
        return JsonResponse({"success": False}, status=406)

    # Create the order
    order = Order.objects.create(
        tab=tab,
        restaurant=cart.restaurant,
        status = Order.StatusType.MADE,
    )
    order.save()

    # Add items to order and remove from cart
    item: Item
    for item in cart.item_set.all(): # type: ignore
        item.order = order
        item.cart = None
        item.save()

    cart.restaurant = None
    cart.save()
    return JsonResponse({"success": True}, status=200)

@require_POST
def cancel(request: HttpRequest) -> HttpResponse:
    if not contains(request.POST, ['order']):
        return JsonResponse({"success": False}, status=400)

    order = get_object_or_404(Order, id=request.POST['order'])
    order.pending_cancellation = True
    order.save()
    return JsonResponse({"success": True}, status=200)
