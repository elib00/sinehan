from django import template
from django.urls import resolve

register = template.Library()

@register.simple_tag
def is_active(request, url_name):
    return 'bg-gray-700' if resolve(request.path_info).url_name == url_name else 'hover:bg-gray-900'
    