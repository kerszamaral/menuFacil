from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from cart.models import get_cart_length

from tab.models import Tab
from menuFacil.validation import TAB_KEY, TAB_REDIRECT_URL, tab_token_exists, validate_UUID, post_contains_keys

# Create your views here.
def details(request: HttpRequest) -> HttpResponse:
    if not tab_token_exists(request.session, request.user):
        return redirect(TAB_REDIRECT_URL)

    tab = Tab.objects.get(id=request.session[TAB_KEY])
    orders = tab.order_set.all() # type: ignore
    orders = orders.order_by('-created_at').reverse()
    ctx = {
            'orders': orders,
            'cart_length': get_cart_length(request.session, request.user)
        }

    return render(request, 'tab/details.html', ctx)

def present(request: HttpRequest):
    if request.method != "POST":
        return render(request, 'tab/present.html')

    if not post_contains_keys(request.POST, ['tab']) or \
       not validate_UUID(request.POST['tab']) or \
       not Tab.objects.filter(id=request.POST['tab']).exists():
        return JsonResponse({"success": False}, status=400)

    request.session[TAB_KEY] = request.POST['tab']

    return JsonResponse({"success": True}, status=200)


# def pay_tab():
