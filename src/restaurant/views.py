import io
from typing import Any
from uuid import UUID
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import FileResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

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

def get_qrcode(request: HttpRequest, tab_id: UUID):
    template = get_template('restaurant/qrcode.html')
    html = template.render({'tab_id': tab_id})
    buffer = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), buffer)
    buffer.seek(0)
    if not pdf.err:
        return FileResponse(buffer, as_attachment=True, filename= str(tab_id).split('-')[0] + ".pdf")
