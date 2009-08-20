"""
    URL Pattern List for Author module
"""

from django.conf.urls.defaults import patterns

urlpatterns = patterns('',
    
    # upload form
    (r'^upload[/]$', 'pbsite.author.views.upload'),            
)
