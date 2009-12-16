from django import template
from podiobooks.main.models import *
from podiobooks.settings import MEDIA_URL
register = template.Library()

@register.inclusion_tag('main/tags/show_heading.html')
def show_heading(text):
    return { 'text' : text, 'MEDIA_URL': MEDIA_URL}
