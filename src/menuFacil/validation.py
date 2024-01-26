import uuid
from django.apps import apps
from django.contrib.auth.models import AbstractBaseUser, AnonymousUser
from django.contrib.sessions.backends.base import SessionBase

CART_KEY = 'cart_token'
TAB_KEY = 'tab_token'
CART_REDIRECT_URL = "cart:create"
TAB_REDIRECT_URL = "tab:present"


def cart_token_exists(session: SessionBase, user: AbstractBaseUser | AnonymousUser) -> bool:
    if user.is_authenticated:
        session[CART_KEY] = str(user.cart.id) # type: ignore
        return True

    if CART_KEY in session.keys():
        return True

    model = apps.get_model(app_label='cart', model_name='Cart')
    cart = model.objects.create()
    session[CART_KEY] = str(cart.id) # type: ignore
    return True

def tab_token_exists(session: SessionBase, user: AbstractBaseUser | AnonymousUser) -> bool:
    if user.is_authenticated:
        session[TAB_KEY] = str(user.tab.id) # type: ignore
        return True

    if TAB_KEY in session.keys():
        return True

    return False

def validate_UUID(uuid_to_test: str) -> bool:
    try:
        uuid.UUID(uuid_to_test)
        return True
    except ValueError:
        return False