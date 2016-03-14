from django import template
from django.utils.safestring import mark_safe
from django.template.defaultfilters import stringfilter
from urllib.parse import unquote

register = template.Library()

@register.filter(is_safe=True)
def raw_url(url):
    print (url)
    return mark_safe(url)

@register.filter()
@stringfilter
def unquote_raw(value):
    print (unquote(value))
    return unquote(value)
