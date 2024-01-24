from uuid import UUID
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from cart.models import Item
from tab.models import Tab
from validation import cart_token_exists, tab_token_exists, CART_KEY, TAB_KEY, CART_REDIRECT_URL, TAB_REDIRECT_URL
from .models import Order

# Create your views here.
def create_order(request: HttpRequest) -> HttpResponse:
    if not cart_token_exists(request):
        return redirect(CART_REDIRECT_URL)
    cart_token = request.session[CART_KEY]
    
    if not tab_token_exists(request):
        return redirect(TAB_REDIRECT_URL)
    tab_token = request.session[TAB_KEY]
    
    cart_items = Item.objects.filter(cart_id=cart_token)
    tab = Tab.objects.get(id=request.session[tab_token])
    
    restaurant = cart_items.first().food.menu.restaurant
    order = Order.objects.create(
        tab=tab,
        restaurant=restaurant,
        total_price=sum(item.price for item in cart_items),
        status = Order.StatusType.MADE,
    )
    order.save()
    for item in cart_items:
        order.item_set.create(
            food=item.food,
            quantity=item.quantity,
            price=item.price,
        )
    cart_items.delete()
    #! Handle cart recreation
    return render(request, 'order/validate.html') #! Change from validate

def cancel_order(request: HttpRequest, order_id: UUID) -> HttpResponse:
    if not cart_token_exists(request):
        return redirect(CART_REDIRECT_URL)
    
    order = get_object_or_404(Order, id=order_id)
    order.pending_cancellation = True
    order.save()
    return redirect('order:list_orders') #! Change from list orders
