from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.contrib.messages import get_messages
from cart.models import get_cart_length

from tab.models import Tab
from menuFacil.validation import TAB_KEY, TAB_REDIRECT_URL, tab_token_exists

# Create your views here.
def list_orders_in_tab(request: HttpRequest) -> HttpResponse:
    if not tab_token_exists(request.session, request.user):
        return redirect(TAB_REDIRECT_URL)

    tab = Tab.objects.get(id=request.session[TAB_KEY])
    orders = tab.order_set.all() # type: ignore
    orders = orders.order_by('-created_at')
    ctx = {
            'orders': orders,
            'messages':get_messages(request),
            'cart_length': get_cart_length(request.session, request.user)
        }

    return render(request, 'tab/details.html', ctx)

def present_tab(request: HttpRequest):
    return render(request, 'tab/present.html')

# def pay_tab():
