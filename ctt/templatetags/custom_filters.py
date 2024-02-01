from django import template
from django.utils.safestring import SafeString

register = template.Library()

@register.filter(name='get_type')
def get_type(value, SafeString):
    return type(value).__name__ == SafeString