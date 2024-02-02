from django import template

register = template.Library()

@register.filter
def filter_name(dict_data, key):
    if key:
        return dict_data.filter(name__startswith=key)
    return dict_data

@register.filter
def get_item(dict_data, key):
    if key:
        return dict_data.get(key, "")