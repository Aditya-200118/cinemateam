from django import template
from django.utils.safestring import SafeString

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    if isinstance(field, SafeString):
        return field
    return field.as_widget(attrs={"class": css_class})

@register.filter(name='attr')
def attr(field, args):
    if isinstance(field, SafeString):
        return field
    attrs = {}
    definition = args.split(',')
    for d in definition:
        key, val = d.split(':')
        attrs[key] = val
    return field.as_widget(attrs=attrs)
