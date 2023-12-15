from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

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

class MenuAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['restaurant', 'name']}),
    ]
    inlines = [FoodInline]
    list_display = ('restaurant', 'name')
    list_filter = ['restaurant']
    search_fields = ['name']

class MenuInline(admin.TabularInline, EditLinkToInlineObject):
    model = Menu
    extra = 0
    readonly_fields = ('edit_link',)

class RestaurantAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'address', 'phone']}),
    ]
    inlines = [MenuInline]

admin.site.register(Menu, MenuAdmin)
admin.site.register(Restaurant, RestaurantAdmin)
