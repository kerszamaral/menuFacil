from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from guardian.admin import GuardedModelAdmin
from guardian.core import ObjectPermissionChecker

from .models import Restaurant, Menu, Food

class EditLinkToInlineObject(object):
    def edit_link(self, instance):
        url = reverse(f"admin:{instance._meta.app_label}_{instance._meta.model_name}_change",
                      args=[instance.pk] )
        if instance.pk:
            return mark_safe(u'<a href="{u}">edit</a>'.format(u=url))
        else:
            return ''

# Register your models here.
class FoodInline(admin.TabularInline):
    model = Food
    extra = 1

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    inlines = [FoodInline]
    list_display = ('restaurant', 'name')
    list_filter = ['restaurant']
    search_fields = ['name']

    def has_module_permission(self, request):
        return False

class MenuInline(admin.TabularInline, EditLinkToInlineObject):
    model = Menu
    extra = 0
    readonly_fields = ('edit_link',)

@admin.register(Restaurant)
class RestaurantAdmin(GuardedModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'address', 'phone', 'logo']}),
    ]
    inlines = [MenuInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs

        for restaurant in qs:
            if not request.user.has_perm('restaurant.view_restaurant', restaurant):
                qs = qs.exclude(pk=restaurant.pk)

        return qs
