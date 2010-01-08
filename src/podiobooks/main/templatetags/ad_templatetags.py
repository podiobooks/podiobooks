""" Global Tags """

from django import template
from podiobooks.settings import MEDIA_URL

register = template.Library()

@register.inclusion_tag('main/ad/tags/ad_placeholder.html')
def ad_placeholder():
    return {'MEDIA_URL': MEDIA_URL}