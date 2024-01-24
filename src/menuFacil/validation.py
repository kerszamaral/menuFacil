
from django.http import HttpRequest
from django.apps import apps

CART_KEY = 'cart_token'
TAB_KEY = 'tab_token'
CART_REDIRECT_URL = "cart:create"
TAB_REDIRECT_URL = "BBBB"

def cart_token_exists(request: HttpRequest) -> bool:
    if request.user.is_authenticated:
        cart = request.user.cart # type: ignore
        request.session[CART_KEY] = cart.id
        return True
    
    if CART_KEY in request.session.keys():
        return True
    
    model = apps.get_model(app_label='cart', model_name='Cart')
    cart = model.objects.create()
    request.session[CART_KEY] = cart.id # type: ignore
    return True

def tab_token_exists(request: HttpRequest) -> bool:
    if TAB_KEY in request.session.keys():
        return True

    if request.user.is_authenticated:
        tab = request.user.tab # type: ignore
        request.session[TAB_KEY] = tab.id
        return True

    return False
