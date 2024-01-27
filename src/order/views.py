from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

from item.models import Item
from cart.models import Cart
from tab.models import Tab
from menuFacil.validation import tab_token_exists, TAB_KEY, post_contains_keys
from .models import Order

# Create your views here.
@require_POST
def create(request: HttpRequest) -> HttpResponse:
    if not post_contains_keys(request.POST, ['cart']):
        return JsonResponse({"success": False}, status=400)

    if not tab_token_exists(request.session, request.user):
        return JsonResponse({"success": False}, status=412)

    cart = Cart.objects.get(id=request.POST['cart'])
    tab = Tab.objects.get(id=request.session[TAB_KEY])

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
    if not post_contains_keys(request.POST, ['order']):
        return JsonResponse({"success": False}, status=400)

    order = get_object_or_404(Order, id=request.POST['order'])
    order.pending_cancellation = True
    order.save()
    return JsonResponse({"success": True}, status=200)
