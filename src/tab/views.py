from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from cart.models import get_cart_length

from tab.models import Tab
from menuFacil.validation import TAB_KEY, TAB_REDIRECT_URL, tab_token_exists, validate_UUID

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
    if request.method == "POST":
        if not validate_UUID(request.POST['data']):
            response = JsonResponse({"success": False})
            response.status_code = 400
            return response

        tab_id = request.POST['data']

        try:
            tab = Tab.objects.get(id=tab_id)
        except Tab.DoesNotExist:
            response = JsonResponse({"success": False})
            response.status_code = 404
            return response

        request.session[TAB_KEY] = str(tab.id) # type: ignore

        response = JsonResponse({"success": True})
        response.status_code = 200 # To announce that the user isn't allowed to publish
        return response

    return render(request, 'tab/present.html')

# def pay_tab():
