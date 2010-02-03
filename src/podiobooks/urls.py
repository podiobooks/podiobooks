"""
    Master URL Pattern List for the application.  Most of the patterns here should be top-level
    pass-offs to sub-modules, who will have their own urls.py defining actions within.
"""

from django.conf.urls.defaults import * #@UnusedWildImport
from django.contrib import admin
from settings import DEBUG, MEDIA_ROOT

admin.autodiscover()

urlpatterns = patterns('',
    # Home Page
    url(r'^$', 'podiobooks.main.views.index', name="home_page"),
                       
    # URLs from main package
    (r'^', include('podiobooks.main.urls')),

    # Admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Admin Site:
    (r'^admin/', include(admin.site.urls)),
    
    # authopenid
    (r'^account/', include('django_authopenid.urls')),                     
    
    # Feeds:
    (r'^rss/', include('podiobooks.feeds.urls')),
    
    # Author Interface:
    (r'^author/', include('podiobooks.author.urls')),
    
    #TinyMCE WYSIWYG HTML Editor:
    (r'^tinymce/', include('tinymce.urls')),
    
    # Social Media Views
    (r'^social/', include('podiobooks.social.urls')),
    
    # Django Comments
    (r'^comments/', include('django.contrib.comments.urls')),
    
)

#Only hook up the media to run through Django in a dev environment...in prod, needs to be handled by web server
if DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT, 'show_indexes': True}),
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
