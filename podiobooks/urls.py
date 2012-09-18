"""
    Master URL Pattern List for the application.  Most of the patterns here should be top-level
    pass-offs to sub-modules, who will have their own urls.py defining actions within.
"""

# pylint: disable=E1120

from django.conf.urls import patterns, url, include
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.views.generic import RedirectView
from .views import BlogRedirectView, TextTemplateView, RobotsView

admin.autodiscover()

urlpatterns = patterns('',
    # Home Page
    url(r'^$', 'podiobooks.core.views.index', name="home_page"),
                       
    # URLs from core package
    (r'^', include('podiobooks.core.urls')),

    # Admin documentation
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Admin Site
    (r'^admin/', include(admin.site.urls)),
    
    # Auth / Login
    (r'^account/signin/$', 'django.contrib.auth.views.login'),

    # Django Comments
    (r'^comments/', include('django.contrib.comments.urls')),
    
    # Feeds
    (r'^rss/', include('podiobooks.feeds.urls')),

    # Robots, Favicon and Related
    (r'^robots\.txt$', RobotsView.as_view()),
    (r'^favicon\.ico$', RedirectView.as_view(url=settings.STATIC_URL + 'images/favicon.ico')),
    (r'^humans\.txt$', TextTemplateView.as_view(template_name='humans.txt')),
    (r'^crossdomain\.xml', TextTemplateView.as_view(template_name='crossdomain.xml')),

    # Blog
    (r'^blog(?P<url_remainder>.*)', BlogRedirectView.as_view()),

    # PB1 Search Redirect
    (r'podiobooks/search\.php', RedirectView.as_view(url='/title/search/', query_string=True)),

    # PB1 Authors Doc
    (r'authors/PBAuthoringGuidev2\.0\.4\.pdf', RedirectView.as_view(url='http://blog.podiobooks.com/wp-content/uploads/2012/09/PBAuthoringGuidev2.0.4.pdf')),

    # PB1 Login Page
    (r'login\.php|Xlogin\.php', RedirectView.as_view(url='http://blog.podiobooks.com/what-happened-to-my-login/')),

    # PB1 Charts Page
    (r'charts\.php', RedirectView.as_view(url='http://blog.podiobooks.com/what-happened-to-the-charts/')),

)

#Only hook up the static and media to run through Django in a dev environment...in prod, needs to be handled by web server
if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT
            }),
    )