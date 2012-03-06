""" Django Custom Template Tags for Advertising-Related Stuff """

from django import template

register = template.Library()

@register.inclusion_tag('core/ad/tags/ad_placeholder.html')
def ad_placeholder():
    """Placeholder for Future Ads"""
    return { }
