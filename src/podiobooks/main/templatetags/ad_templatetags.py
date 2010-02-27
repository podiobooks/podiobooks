""" Global Tags """

from django import template
from django.conf import settings

register = template.Library()

@register.inclusion_tag('main/ad/tags/ad_placeholder.html')
def ad_placeholder():
    return {'MEDIA_URL': settings.MEDIA_URL}
