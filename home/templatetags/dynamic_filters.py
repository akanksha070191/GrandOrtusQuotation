from django import template

register = template.Library()
@register.filter
def get_attr(obj, attr):
    if isinstance(obj, dict):
        return obj.get(attr, None)
    return getattr(obj, attr, None)

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
    