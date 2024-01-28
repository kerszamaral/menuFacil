from django import template

from cart.models import Cart, get_cart_length


register = template.Library()

@register.simple_tag
def cart_length(cart, session, user):
    if cart:
        return Cart.objects.get(id=cart).get_length()
    return get_cart_length(session, user)
