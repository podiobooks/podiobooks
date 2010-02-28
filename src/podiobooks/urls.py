"""
    Master URL Pattern List for the application.  Most of the patterns here should be top-level
    pass-offs to sub-modules, who will have their own urls.py defining actions within.
"""

# pylint: disable-msg=E0602,F0401

from django.conf.urls.defaults import * #@UnusedWildImport # pylint: disable-msg=W0401,W0614
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    # Home Page
    url(r'^$', 'podiobooks.main.views.index', name="home_page"),
                       
    # URLs from main package
    (r'^', include('podiobooks.main.urls')),

    # Admin documentation
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Admin Site
    (r'^admin/', include(admin.site.urls)),
    
    # Authopenid
    (r'^account/', include('django_authopenid.urls')),
    
     # Author Interface
    (r'^author/', include('podiobooks.author.urls')),
    
    # Django Comments
    (r'^comments/', include('django.contrib.comments.urls')),
    
    # FAQ
    (r'^faq/', include('faq.urls')),
    
    # Feeds
    (r'^rss/', include('podiobooks.feeds.urls')),
    
    # Haystack Search
    (r'^search/', include('haystack.urls')),

    # Social Media Views
    (r'^social/', include('podiobooks.social.urls')),
    
    # TinyMCE WYSIWYG HTML Editor
    (r'^tinymce/', include('tinymce.urls')),
)
    
# Databrowse setup
from django.contrib import databrowse
from podiobooks.main.models import Category, Contributor, Episode, Title

databrowse.site.register(Category)
databrowse.site.register(Contributor)
databrowse.site.register(Episode)
databrowse.site.register(Title)

urlpatterns += patterns('',
        (r'^db/(.*)', databrowse.site.root),
)
