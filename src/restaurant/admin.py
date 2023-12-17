from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.urls import reverse
from django.utils.safestring import mark_safe
from guardian.admin import GuardedModelAdmin
from guardian.shortcuts import get_objects_for_user
from django_object_actions import DjangoObjectActions

from .models import Restaurant, Menu, Food
from order.models import Order, Item

class LockedModel(object):
    def has_add_permission(self, request, obj=None) -> bool:
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        return False


class HiddenModel(object):
    def has_module_permission(self, request):
        # Hide the model from admin index
        return False

class EditLinkToInlineObject(object):
    def edit_link(self, instance):
        url = reverse(f"admin:{instance._meta.app_label}_{instance._meta.model_name}_change",
                      args=[instance.pk] )
        if instance.pk:
            return mark_safe(u'<a href="{u}">edit</a>'.format(u=url))
        else:
            return ''

class PermissionCheckModelAdmin(GuardedModelAdmin):
    def has_module_permission(self, request: HttpRequest) -> bool:
        if super().has_module_permission(request):
            return True
        return self.get_model_objects(request).exists()

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        data = self.get_model_objects(request)
        return data

    def get_model_objects(self, request: HttpRequest, action=None, klass=None):
        opts = self.opts
        actions = [action] if action else ['view', 'add', 'change', 'delete']
        klass = klass or opts.model
        model_name = klass._meta.model_name
        return get_objects_for_user(user=request.user, 
                                    perms=[f'{perm}_{model_name}' for perm in actions], 
                                    klass=klass, any_perm=True)

    def has_permission(self, request: HttpRequest, obj, action) -> bool:
        opts = self.opts
        code_name = f'{action}_{opts.model_name}'
        if obj:
            return request.user.has_perm(f'{opts.app_label}.{code_name}', obj)
        else:
            return self.get_model_objects(request).exists()

    def has_view_permission(self, request, obj=None):
        return self.has_permission(request, obj, 'view')

    def has_change_permission(self, request, obj=None):
        return self.has_permission(request, obj, 'change')

    def has_delete_permission(self, request, obj=None):
        return self.has_permission(request, obj, 'delete')

# Register your models here.
class FoodInline(admin.TabularInline):
    model = Food
    extra = 1

@admin.register(Menu)
class MenuAdmin(HiddenModel, admin.ModelAdmin):
    inlines = [FoodInline]
    list_display = ('restaurant', 'name')
    list_filter = ['restaurant']
    search_fields = ['name']


class ItemInline(LockedModel, admin.TabularInline):
    model = Item
    extra = 0
    can_delete = False
    readonly_fields = ('food', 'quantity', 'price')

@admin.register(Order)
class OrderAdmin(DjangoObjectActions, HiddenModel, LockedModel, admin.ModelAdmin, EditLinkToInlineObject):
    inlines = [ItemInline]
    readonly_fields = ('pending_cancellation', 'payed',
                       'client', 'total_price', 'created_at',
                       'updated_at')

    def approve_cancellation(self, request, obj):
        if obj.pending_cancellation and obj.status == Order.StatusType.OPEN:
            obj.status = Order.StatusType.CANCELLED
            obj.save()
            self.message_user(request, "Order cancelled")
        else:
            self.message_user(request, "Order not pending cancellation")
            
    def approve_payment(self, request, obj):
        if not obj.payed and not obj.status == Order.StatusType.OPEN and not obj.status == Order.StatusType.CANCELLED and not obj.pending_cancellation:
            obj.payed = True
            obj.save()
            self.message_user(request, "Order payed")
        else:
            self.message_user(request, "Unable to pay order")

    change_actions = ('approve_cancellation', 'approve_payment')

class OrdersInline(LockedModel, admin.TabularInline):
    model = Order
    extra = 0

    can_delete = False
    readonly_fields = ('pending_cancellation', 'payed',
                       'client', 'total_price', 'created_at',
                       'updated_at', 'details_link')

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        qs = super().get_queryset(request)
        qs = qs.exclude(status=Order.StatusType.MADE
              ).exclude(status=Order.StatusType.IN_PROGRESS)
        return qs.order_by('-created_at')

    def details_link(self, instance):
        url = reverse(f"admin:{instance._meta.app_label}_{instance._meta.model_name}_change",
                      args=[instance.pk] )
        if instance.pk:
            return mark_safe(u'<a href="{u}">details</a>'.format(u=url))
        else:
            return ''

class MakingOrdersInline(OrdersInline):
    verbose_name = "Order in the Making"
    def get_queryset(self, request: HttpRequest) -> QuerySet:
        qs = super(OrdersInline, self).get_queryset(request)
        qs = qs.exclude(status=Order.StatusType.OPEN
              ).exclude(status=Order.StatusType.CANCELLED    
              ).exclude(status=Order.StatusType.DELIVERED)
        return qs.order_by('-updated_at')

class MenuInline(admin.TabularInline, EditLinkToInlineObject):
    model = Menu
    extra = 0
    readonly_fields = ('edit_link',)

@admin.register(Restaurant)
class RestaurantAdmin(PermissionCheckModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'address', 'phone', 'logo', 'message']}),
    ]
    inlines = [MenuInline, MakingOrdersInline, OrdersInline]
