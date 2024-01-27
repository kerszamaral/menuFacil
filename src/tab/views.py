from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from tab.models import HistoricTab, Tab
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
            'tab': tab,
        }

    return render(request, 'tab/details.html', ctx)

def present(request: HttpRequest) -> HttpResponse:
    if request.method != "POST":
        return render(request, 'tab/present.html')

    if not post_contains_keys(request.POST, ['tab']) or \
       not validate_UUID(request.POST['tab']) or \
       not Tab.objects.filter(id=request.POST['tab']).exists():
        return JsonResponse({"success": False}, status=400)

    request.session[TAB_KEY] = request.POST['tab']

    return JsonResponse({"success": True}, status=200)

@login_required(login_url="/account/login/")
def history(request: HttpRequest) -> HttpResponse:
    ctx = {
            'historic_tabs': HistoricTab.objects.filter(client=request.user).order_by('-created_at').reverse()
        }

    return render(request, 'tab/history.html', ctx)

@require_POST
def payed(request: HttpRequest) -> HttpResponse:
    if not post_contains_keys(request.POST, ['tab']):
        return JsonResponse({"success": False}, status=400)

    tab = get_object_or_404(Tab, id=request.POST['tab'])
    if tab.client is None:
        tab.order_set.clear() # type: ignore
        tab.save()
        return JsonResponse({"success": True}, status=200)

    historic = HistoricTab.objects.create(
        client=tab.client
    )
    for order in tab.order_set.all(): # type: ignore
        historic.order_set.add(order) # type: ignore
        order.tab = None
        order.save()

    historic.save()

    tab.restaurant = None
    tab.save()
    return JsonResponse({"success": True}, status=200)
