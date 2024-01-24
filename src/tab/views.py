from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.contrib.messages import get_messages
from cart.models import Cart

from tab.models import Tab
from order.models import Order
from validation import TAB_KEY, TAB_REDIRECT_URL, tab_token_exists

# Create your views here.

# localhost:8000/tab/orders
# cliente -> request dizendo "Quero essa pagina, ta aqui minhas informações"
# servidor processa request -> response "ta aqui o que eu tenho para te mostrar em html"
def list_orders_in_tab(request: HttpRequest) -> HttpResponse:
    if not tab_token_exists(request):
        return redirect(TAB_REDIRECT_URL)
    
    tab = Tab.objects.get(id=request.session[TAB_KEY])
    orders = Order.objects.filter(tab=tab)
    orders = orders.order_by('-created_at')
    ctx = {
            'orders': orders,
            "open": Order.StatusType.OPEN,
            'messages':get_messages(request),
            'cart_length': Cart.get_length(request)
        }
    
    return render(request, 'order/list.html', ctx)