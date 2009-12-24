from django import template
from podiobooks.main.models import *
from podiobooks.main.views import *
from podiobooks.settings import MEDIA_URL
register = template.Library()

@register.inclusion_tag('main/tags/show_heading.html')
def show_heading(text):
    return { 'text' : text, 'MEDIA_URL': MEDIA_URL}

@register.inclusion_tag('main/tags/show_searchbox.html')
def show_searchbox():
    return { 'categoryChoiceForm':CategoryChoiceForm(), 'titleQuickSearchForm': TitleQuickSearchForm(), 'MEDIA_URL': MEDIA_URL}

