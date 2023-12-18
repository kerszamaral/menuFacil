"""
URL configuration for menuFacil project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve

from . import views
from menuFacil import settings

admin.site.site_title = "Menu Fácil site admin"
admin.site.site_header = "Menu Fácil administration"
admin.site.index_title = "Menu Fácil administration"

urlpatterns = [
    path("", views.index, name="home"),
    path("account/", include("account.urls")),
    path('admin/', admin.site.urls),
    path("cart/", include("cart.urls")),
    path("order/", include("order.urls")),
    path("restaurant/", include("restaurant.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    urlpatterns += [re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT})]
    urlpatterns += [re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT})]
