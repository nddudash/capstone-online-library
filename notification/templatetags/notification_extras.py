from django import template

register = template.Library()

# CITATION -https://stackoverflow.com/questions/2970244/django-templates-value-of-dictionary-key-with-a-space-in-it


@register.filter
def get_exclamation(mapping):
        return mapping.filter(exclamation = True)
