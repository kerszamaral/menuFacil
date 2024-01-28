from typing import Any
from django.contrib import admin, messages
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.shortcuts import redirect, resolve_url
from django.urls import resolve, reverse
from django.utils.safestring import mark_safe
from guardian.admin import GuardedModelAdmin
from guardian.shortcuts import get_objects_for_user
from guardian.core import ObjectPermissionChecker
from django_object_actions import DjangoObjectActions


from order.models import Order
from item.models import Item
from tab.models import Tab
from .models import Promotion, Restaurant, Menu, Food

class LockedModel(object):
    def has_add_permission(self, request, obj=None) -> bool: # pylint: disable=unused-argument
        return False

    def has_delete_permission(self, request, obj=None) -> bool:  # pylint: disable=unused-argument
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
            return mark_safe(f'<a href="{url}">edit</a>')
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
            return request.user.has_perm(f'{opts.app_label}.{code_name}', obj) # type: ignore
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
    list_display = ('name', 'price')
    extra = 1

@admin.register(Menu)
class MenuAdmin(HiddenModel, admin.ModelAdmin):
    inlines = [FoodInline]
    list_display = ('restaurant', 'name')
    list_filter = ['restaurant']
    search_fields = ['name']

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        if request.user.is_superuser:
            return super().get_queryset(request)
        return Menu.objects.none()

class ItemInline(LockedModel, admin.TabularInline):
    model = Item
    extra = 0
    can_delete = False
    readonly_fields = ('cart', 'food', 'quantity', 'price')

@admin.register(Order)
class OrderAdmin(DjangoObjectActions, HiddenModel, LockedModel, GuardedModelAdmin):
    inlines = [ItemInline]
    readonly_fields = ('status', 
                       'pending_cancellation',
                       'created_at',
                       'updated_at')

    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
        if obj.status == Order.StatusType.CANCELLED:
            self.message_user(request, "You don't have permission to cancel this order")
            return
        return super().save_model(request, obj, form, change)

    def get_model_objects(self, request: HttpRequest, action=None, klass=None):
        opts = self.opts
        actions = [action] if action else ['view', 'add', 'change', 'delete']
        klass = klass or opts.model
        model_name = klass._meta.model_name
        return get_objects_for_user(user=request.user,
                                    perms=[f'{perm}_{model_name}' for perm in actions],
                                    klass=klass, any_perm=True)

    def approve_cancellation(self, request, obj):
        if not self.get_model_objects(request, action='delete').exists():
            self.message_user(request, "You don't have permission to cancel this order")
            return
        if obj.pending_cancellation and obj.status in [Order.StatusType.MADE, Order.StatusType.IN_PROGRESS]:
            obj.status = Order.StatusType.CANCELLED
            obj.save()
            self.message_user(request, "Order cancelled")
        else:
            self.message_user(request, "Order not pending cancellation")

    def in_progress(self, request, obj):
        if obj.status == Order.StatusType.MADE:
            obj.status = Order.StatusType.IN_PROGRESS
            obj.save()
            self.message_user(request, "Order in progress")
        else:
            self.message_user(request, "Couldn't change order status")

    def delivered(self, request, obj):
        if obj.status == Order.StatusType.IN_PROGRESS:
            obj.status = Order.StatusType.DELIVERED
            obj.save()
            self.message_user(request, "Order delivered")
        else:
            self.message_user(request, "Couldn't change order status")

    change_actions = ('approve_cancellation','in_progress', 'delivered')
    
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        if request.user.is_superuser:
            return super().get_queryset(request)
        return Order.objects.none()

class OrdersInline(LockedModel, admin.TabularInline):
    model = Order
    extra = 0

    can_delete = False
    readonly_fields = ('status',
                       'pending_cancellation',
                       'created_at',
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
            return mark_safe(f'<a href="{url}">edit</a>')
        else:
            return ''

class MakingOrdersInline(OrdersInline):
    verbose_name = "Order in the Making"
    def get_queryset(self, request: HttpRequest) -> QuerySet:
        qs = super(OrdersInline, self).get_queryset(request)
        qs = qs.exclude(status=Order.StatusType.CANCELLED
              ).exclude(status=Order.StatusType.DELIVERED)
        return qs.order_by('-updated_at')

class PromotionInline(admin.TabularInline):
    model = Promotion
    extra = 0
    filter_horizontal = ('menu',)
    
    def get_parent_object_from_request(self, request):
        """
        Returns the parent object from the request or None.

        Note that this only works for Inlines, because the `parent_model`
        is not available in the regular admin.ModelAdmin as an attribute.
        """
        resolved = resolve(request.path_info)
        if resolved.kwargs:
            return self.parent_model.objects.get(pk=resolved.kwargs['object_id'])
        return None
    
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        kwargs['queryset'] = Menu.objects.filter(restaurant=self.get_parent_object_from_request(request))
        return super().formfield_for_manytomany(db_field, request, **kwargs)


class MenuInline(admin.TabularInline, EditLinkToInlineObject):
    model = Menu
    extra = 0
    readonly_fields = ('edit_link',)

class TabInline(admin.TabularInline):
    model = Tab
    extra = 0
    max_num = 0
    readonly_fields = ('get_qrcode', )

    def get_qrcode(self, instance):
        if instance.pk:
            url = resolve_url('restaurant:qrcode', tab_id=str(instance.pk))
            return mark_safe(f'<a href="{url}">Get QRCode</a>')
        return ''


@admin.register(Restaurant)
class RestaurantAdmin(DjangoObjectActions, PermissionCheckModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'address', 'phone', 'logo', 'message']}),
    ]
    change_actions = ['object_permissions', 'create_tab', 'generate_sales_report' ]
    inlines = [MenuInline, PromotionInline, MakingOrdersInline, OrdersInline, TabInline]

    def create_tab(self, request: HttpRequest, obj):
        if not self.get_model_objects(request, action='add', klass=Tab).exists():
            self.message_user(request, "You don't have permission to create tabs")
            return
        Tab.objects.create(restaurant=obj)
        messages.success(request, 'Tab created')

    def generate_sales_report(self, request: HttpRequest, obj):
        if not self.get_model_objects(request, action='add', klass=Menu).exists():
            self.message_user(request, "You don't have permission to see sales report")
            return
        return redirect(reverse('restaurant:sales', args=[obj.pk]))

    # Needed because of bug in django-object-actions
    def object_permissions(self, request: HttpRequest, obj):
        if not ObjectPermissionChecker(request.user).has_perm('delete_restaurant', obj):
            self.message_user(request, "You don't have permission to change permissions")
            return
        return redirect(reverse(f"admin:{obj._meta.app_label}_{obj._meta.model_name}_permissions",
                      args=[obj.pk] ))
