from django import template
from podiobooks.main.models import *
register = template.Library()

@register.inclusion_tag('main/tags/show_heading.html', takes_context=True)
def show_heading(text):
    return { 'text' : text}
