from django import template
from django.template.defaultfilters import floatformat

register = template.Library()


@register.filter
def percent(value):
    print(value)
    if value is None:
        return None
    else:
        if isinstance(value, str):

            value = float(value)
    return floatformat(value * 100.0, 1) + '%'
