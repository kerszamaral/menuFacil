import io
from typing import Any
from uuid import UUID
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import FileResponse
from django.template.loader import get_template
from django.views.decorators.http import require_POST
from xhtml2pdf import pisa

from menuFacil.validation import contains
from .models import Restaurant

# Create your views here.
class RestaurantsView(generic.ListView):
    template_name = 'restaurant/index.html'
    context_object_name = 'restaurant_list'

    def get_queryset(self) -> QuerySet[Any]:
        return Restaurant.objects.order_by('name')

def menu(request: HttpRequest, restaurant_id: UUID) -> HttpResponse:
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)

    return render(request, 'restaurant/detail.html', {'restaurant': restaurant})

def create_pdf(html, name: str) -> FileResponse:
    buffer = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), buffer)
    buffer.seek(0)
    if not pdf.err: # type: ignore
        return FileResponse(buffer, as_attachment=True, filename= f"{name}.pdf")
    return FileResponse('Error Rendering PDF', status=400)

def get_qrcode(request: HttpRequest, tab_id: UUID) -> FileResponse:
    html = get_template('restaurant/qrcode.html').render({'tab_id': str(tab_id)})
    return create_pdf(html, f"{str(tab_id).split('-')[0]}-qrcode")

def sales(request: HttpRequest, restaurant_id: UUID):
    restaurant = Restaurant.objects.get(pk=restaurant_id)
    html = get_template('restaurant/sales.html').render({'restaurant': restaurant})
    return create_pdf(html, f"{restaurant.name}-sales")

@require_POST
def search(request: HttpRequest) -> HttpResponse:
    if not contains(request.POST, ['search']):
        return JsonResponse({"success": False}, status=400)
    
    request.session['search'] = request.POST['search']

    return JsonResponse({"success": True}, status=200)