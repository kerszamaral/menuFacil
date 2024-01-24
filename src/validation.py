
from django.http import HttpRequest

CART_KEY = 'cart_token'
TAB_KEY = 'tab_token'
CART_REDIRECT_URL = "AAAA"
TAB_REDIRECT_URL = "BBBB"

def cart_token_exists(request: HttpRequest) -> bool:
    return CART_KEY in request.session.keys()

def tab_token_exists(request: HttpRequest) -> bool:
    return TAB_KEY in request.session.keys()