from django import template
from podiobooks.main.models import *
register = template.Library()

@register.inclusion_tag('main/title/tags/show_categories.html')
def show_categories(title):
    categories = title.categories.all()
    return { 'categories' : categories }

@register.inclusion_tag('main/title/tags/show_contributors.html')
def show_contributors(title):
    contributors = title.contributors.all()
    return { 'contributors' : contributors }
