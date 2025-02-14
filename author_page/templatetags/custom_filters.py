import base64
from django import template

register = template.Library()

@register.filter
def b64encode(value):
    if isinstance(value, (bytes, bytearray)):
        return base64.b64encode(value).decode('utf-8')
    return value
