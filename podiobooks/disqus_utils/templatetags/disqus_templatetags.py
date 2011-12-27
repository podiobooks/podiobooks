""" Tags used for working with DISQUS """

from django import template
from django.conf import settings

register = template.Library()

@register.inclusion_tag('disqus_utils/tags/show_disqus_comments.html')
def show_disqus_comments(disqus_identifier, disqus_title, site_url, disqus_url):
    """ Insert the DISQUS Code onto the page """
        
    return {'disqus_identifier': disqus_identifier,
            'disqus_title': disqus_title,
            'disqus_url': site_url + disqus_url,
            'DISQUS_WEBSITE_SHORTNAME': settings.DISQUS_WEBSITE_SHORTNAME,
            'MEDIA_URL': settings.MEDIA_URL,
            'THEME_MEDIA_URL': settings.THEME_MEDIA_URL, }
    
@register.inclusion_tag('disqus_utils/tags/show_disqus_comment_counts.html')   
def show_disqus_comment_count():
    """ Pull the counts for each post so they can be displayed in a list """
    
    return {'DISQUS_WEBSITE_SHORTNAME': settings.DISQUS_WEBSITE_SHORTNAME,
            'MEDIA_URL': settings.MEDIA_URL,
            'THEME_MEDIA_URL': settings.THEME_MEDIA_URL, }