from django import template

register = template.Library()

@register.filter
def get_item(dict_data, key):
    if key:
        return dict_data.get(key, '')
