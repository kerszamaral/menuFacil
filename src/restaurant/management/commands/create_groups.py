from typing import Any
from django.core.management import BaseCommand
from django.contrib.auth.models import Group, Permission

from restaurant import models as restaurant_models
from order import models as order_models
from item import models as item_models
from tab import models as tab_models

GROUPS_PERMISSIONS = {
    'owner': {
        "userobjectpermission": ['add', 'change', 'delete', 'view'],
        restaurant_models.Promotion: ['add', 'change', 'delete', 'view'],
        restaurant_models.Menu: ['add', 'change', 'delete', 'view'],
        restaurant_models.Food: ['add', 'change', 'delete', 'view'],
        order_models.Order: ['change', 'view', 'delete'],
        tab_models.Tab: ['add', 'view'],
        item_models.Item: ['view'],
    },
    'manager': {
        restaurant_models.Promotion: ['add', 'change', 'delete', 'view'],
        restaurant_models.Menu: ['add', 'change', 'delete', 'view'],
        restaurant_models.Food: ['add', 'change', 'delete', 'view'],
        order_models.Order: ['change', 'view', 'delete'],
        tab_models.Tab: ['add', 'view'],
        item_models.Item: ['view'],
    },
    'employee': {
        restaurant_models.Promotion: ['view'],
        restaurant_models.Menu: ['view'],
        restaurant_models.Food: ['view'],
        order_models.Order: ['change', 'view'],
        tab_models.Tab: ['view'],
        item_models.Item: ['view'],
    },
}

class Command(BaseCommand):
    help = "Create default groups"

    def handle(self, *args: Any, **options: Any) -> str | None:
        # Loop groups
        for groups in GROUPS_PERMISSIONS.items():
            group_name = groups[0]
            # Get or create group
            group, _ = Group.objects.get_or_create(name=group_name)
            # Loop models in group
            for model_cls in GROUPS_PERMISSIONS[group_name]:
                # Loop permissions in group/model
                for perm_name in GROUPS_PERMISSIONS[group_name][model_cls]:
                    
                    if isinstance(model_cls, str):
                        codename = perm_name + "_" + model_cls
                    else:
                        codename = perm_name + "_" + model_cls._meta.model_name
                    # assign_perm(codename, group, model_cls)

                    try:
                        # Find permission object and add to group
                        perm = Permission.objects.get(codename=codename)
                        group.permissions.add(perm)
                        self.stdout.write(f"Adding {codename} to group {group}")
                    except Permission.DoesNotExist:
                        self.stdout.write(codename + " not found")
