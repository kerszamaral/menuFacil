from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from order.models import Order

from tab.models import HistoricTab, Tab
from menuFacil.validation import  contains, valid_uuid

TAB_KEY = 'tab_token'

# Create your views here.
def details(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        request.session['tab_token'] = str(request.user.tab.id) # type: ignore

    if 'tab_token' not in request.session.keys():
        return redirect("tab:present")

    tab = Tab.objects.get(id=request.session['tab_token'])
    orders = tab.order.all()
    orders = orders.order_by('-created_at').reverse()
    ctx = {
            'orders': orders,
            'tab': tab,
        }

    return render(request, 'tab/details.html', ctx)

def present(request: HttpRequest) -> HttpResponse:
    if request.method != "POST":
        return render(request, 'tab/present.html')

    if not contains(request.POST, ['tab']) or \
       not valid_uuid(request.POST['tab']) or \
       not Tab.objects.filter(id=request.POST['tab']).exists():
        return JsonResponse({"success": False}, status=400)

    request.session[TAB_KEY] = request.POST['tab']

    return JsonResponse({"success": True}, status=200)

@login_required(login_url="/account/login/")
def history(request: HttpRequest) -> HttpResponse:
    return render(request, 'tab/history.html',
        {
            'historic_tabs': HistoricTab.objects.filter(client=request.user).order_by('-created_at').reverse()
        }
    )

@require_POST
def payed(request: HttpRequest) -> HttpResponse:
    if not contains(request.POST, ['tab']):
        return JsonResponse({"success": False}, status=400)

    tab = get_object_or_404(Tab, id=request.POST['tab'])
    if tab.client is None:
        tab.order.clear()
        tab.save()
        return JsonResponse({"success": True}, status=200)

    historic = HistoricTab.objects.create(
        client=tab.client,
        restaurant=tab.restaurant,
    )
    historic.save()

    order: Order
    for order in tab.order.all():
        order.tab = historic
        order.save()

    tab.restaurant = None
    tab.save()
    return JsonResponse({"success": True}, status=200)
