from uuid import UUID
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect

from item.models import Item
from cart.models import Cart
from tab.models import Tab
from menuFacil.validation import cart_token_exists, tab_token_exists, CART_KEY, TAB_KEY, CART_REDIRECT_URL, TAB_REDIRECT_URL
from .models import Order

# Create your views here.
def create(request: HttpRequest) -> HttpResponse:
    if not cart_token_exists(request.session, request.user):
        return redirect(CART_REDIRECT_URL)
    if not tab_token_exists(request.session, request.user):
        return redirect(TAB_REDIRECT_URL)

    cart = Cart.objects.get(id=request.session[CART_KEY])
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
    return redirect('tab:details')

def cancel(request: HttpRequest, order_id: UUID) -> HttpResponse:
    if not cart_token_exists(request.session, request.user):
        return redirect(CART_REDIRECT_URL)

    order = get_object_or_404(Order, id=order_id)
    order.pending_cancellation = True
    order.save()
    return redirect('tab:details')
