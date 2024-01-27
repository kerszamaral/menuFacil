from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

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

    if not valid_uuid(request.POST['tab']):
        return JsonResponse({"success": False}, status=412)

    try:
        tab = Tab.objects.get(id=request.POST['tab'])
    except KeyError:
        return JsonResponse({"success": False}, status=412)

    restaurant = cart.restaurant # type: ignore

    # Create the order
    order = Order.objects.create(
        tab=tab,
        restaurant=restaurant,
        total_price=cart.get_total_price(),
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
