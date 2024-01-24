
from django.http import HttpRequest

CART_KEY = 'cart_token'
TAB_KEY = 'tab_token'
CART_REDIRECT_URL = "cart:create"
TAB_REDIRECT_URL = "BBBB"

def cart_token_exists(request: HttpRequest) -> bool:
    if CART_KEY in request.session.keys():
        return True

    if request.user.is_authenticated:
        cart = request.user.cart_set.all().first()
        request.session[CART_KEY] = cart.id
        return True

    return False

def tab_token_exists(request: HttpRequest) -> bool:
    if TAB_KEY in request.session.keys():
        return True

    if request.user.is_authenticated:
        tab = request.user.tab_set.all().first()
        request.session[TAB_KEY] = tab.id
        return True

    return False