from django import template

register = template.Library()

# CITATION -https://stackoverflow.com/questions/2970244/django-templates-value-of-dictionary-key-with-a-space-in-it


@register.filter
def get_key(mapping, key):
    return mapping.get(key, '')


@register.filter
def get_readable(mapping):
    readable = mapping.get("text/html; charset=utf-8", '')
    if readable == '':
        readable = mapping.get("text/html; charset=iso-8859-1", '')
    if readable == '':
        readable = mapping.get("text/html", '')
    if readable == '':
        readable = mapping.get("text/plain; charset=utf-8", '')
    if readable == '':
        readable = mapping.get("text/plain", '')

    return readable