from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from order.models import Order

from tab.models import HistoricTab, Tab
from menuFacil.validation import  contains, valid_uuid
from .forms import PaymentForm

TAB_KEY = 'tab_token'

# Create your views here.
def details(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        request.session[TAB_KEY] = str(request.user.tab.id) # type: ignore

    if TAB_KEY not in request.session.keys():
        return redirect("tab:present")

    try:
        tab = Tab.objects.get(id=request.session[TAB_KEY])
    except Tab.DoesNotExist:
        messages.error(request, "Error in getting your Tab")
        request.session.pop(TAB_KEY)
        return redirect("tab:present")

    orders = tab.order.all()
    orders = orders.order_by('-created_at').reverse()
    ctx = {
            'orders': orders,
            'tab': tab,
        }

    return render(request, 'tab/details.html', ctx)

def present(request: HttpRequest) -> HttpResponse:
    if request.method != "POST":
        if TAB_KEY in request.session.keys():
            return redirect("tab:details")
        return render(request, 'tab/present.html')

    if not contains(request.POST, ['tab']) or \
       not valid_uuid(request.POST['tab']) or \
       not Tab.objects.filter(id=request.POST['tab']).exists():
        return JsonResponse({"success": False}, status=400)

    request.session[TAB_KEY] = request.POST['tab']

    return JsonResponse({"success": True}, status=200)

def pay_physical(request: HttpRequest) -> HttpResponse:
    if TAB_KEY not in request.session.keys():
        messages.error(request, "Error in getting your Tab")
        return redirect("tab:details")
    return render(request, 'tab/physical.html', {"tab_id": request.session[TAB_KEY]})

@require_http_methods(["GET", "POST"])
def pay_online(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            if TAB_KEY in request.session.keys():
                if tab_has_been_payed(request.session[TAB_KEY]):
                    return redirect("tab:payed")
        else:
            for error in form.errors:
                print(error)
        messages.error(request, "Error in paying your Tab")
    form = PaymentForm()
    return render(request, 'tab/online.html', {"form": form})

@login_required(login_url="/account/login/")
def history(request: HttpRequest) -> HttpResponse:
    return render(request, 'tab/history.html',
        {
            'historic_tabs': HistoricTab.objects.filter(client=request.user).order_by('-created_at').reverse()
        }
    )

@staff_member_required
def confirm_payment(request: HttpRequest) -> HttpResponse:
    return render(request, 'tab/confirm.html')

@require_http_methods(["GET"])
def remove_tab(request: HttpRequest) -> HttpResponse:
    if TAB_KEY not in request.session.keys():
        messages.error(request, "Error in getting your Tab")
        return redirect("tab:details")

    if Tab.objects.get(id=request.session[TAB_KEY]).order.count() != 0:
        messages.error(request, "Your tab hasn't been paid yet")
        return redirect("tab:details")

    if request.user.is_authenticated:
        messages.error(request, "You can't remove a tab if you are logged in")
        return redirect("tab:details")

    messages.success(request, "Tab Removed Successfully")
    request.session.pop(TAB_KEY)
    return redirect('home')


@require_http_methods(["GET"])
def payed(request: HttpRequest) -> HttpResponse:
    if TAB_KEY not in request.session.keys():
        messages.error(request, "Error in getting your Tab")
        return redirect("tab:details")
    if Tab.objects.get(id=request.session[TAB_KEY]).order.count() == 0:
        messages.success(request, "Tab paid successfully")
        if not request.user.is_authenticated:
            request.session.pop(TAB_KEY)
        return redirect('home')
    messages.error(request, "Tab hasn't been paid yet")
    return redirect("tab:details")


def tab_has_been_payed(tab_id: str) -> bool:
    tab = get_object_or_404(Tab, id=tab_id)

    new_tab: HistoricTab | None
    if tab.client is None:
        new_tab = None
    else:
        new_tab = HistoricTab.objects.create(
            client=tab.client,
            restaurant=tab.restaurant,
        )
        tab.restaurant = None

    order: Order
    for order in tab.order.all():
        order.tab = new_tab
        order.save()

    tab.save()
    return True

@staff_member_required
@require_http_methods(["POST"])
def get_tab_page(request: HttpRequest) -> HttpResponse:
    if not contains(request.POST, ['tab']) or \
       not valid_uuid(request.POST['tab']) or \
       not Tab.objects.filter(id=request.POST['tab']).exists():
        return JsonResponse({"success": False}, status=400)

    url = reverse("admin:tab_tab_change", args=[request.POST['tab']])

    return JsonResponse({"success": True, "redirect": url}, status=200)
