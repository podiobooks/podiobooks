"""
    Master URL Pattern List for the application.  Most of the patterns here should be top-level
    pass-offs to sub-modules, who will have their own urls.py defining actions within.
"""

# pylint: disable=E1120

from django.conf.urls import patterns, url, include
from django.contrib import admin
from django.contrib.auth.views import login as login_view
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.admindocs import urls as admindocs_urls
from django.contrib.sitemaps.views import sitemap as sitemap_urls
from django.views.static import serve as dev_static_views
from django.conf import settings
from django.views.generic import RedirectView
from django.views.decorators.vary import vary_on_headers

from podiobooks.core.sitemaps import AwardDetailSitemap, CategoryDetailSitemap, ContributorDetailSitemap, \
    TitleDetailSitemap
from podiobooks.core.views import AccelView, IndexView, DonationView, ReportsView, NoMediaReportView

from .views import BlogRedirectView, TextTemplateView, RobotsView

admin.autodiscover()

sitemaps = {'AwardDetail': AwardDetailSitemap, 'CategoryDetail': CategoryDetailSitemap,
            'ContributorDetail': ContributorDetailSitemap, 'TitleDetail': TitleDetailSitemap, }

urlpatterns = \
    patterns('',
             # Home Page
             url(r'^$', IndexView.as_view(), name="home_page"),

             # Donation Options View
             url(r'^donate/$', DonationView.as_view(), name='donate'),

             # Recent Titles Feed Redirect
             url(r'^index\.xml$', RedirectView.as_view(url='/rss/feeds/titles/recent/')),

             # URLs from core package
             (r'^', include('podiobooks.core.urls')),

             # Admin documentation
             (r'^admin/doc/', include(admindocs_urls)),

             # Admin reports
             url(r'^admin/reports/$', staff_member_required(ReportsView.as_view()), name='report_list'),
             url(r'^admin/reports/nomedia/$', staff_member_required(NoMediaReportView.as_view()),
                 name='report_nomedia'),

             # Admin Site
             (r'^admin/', include(admin.site.urls)),

             # Auth / Login
             (r'^account/signin/$', login_view),

             # Feeds
             (r'^rss/', include('podiobooks.feeds.urls')),

             # Libsyn Utils
             (r'^libsyn/', include('podiobooks.libsyn.urls')),

             # Ratings
             (r'^rate/', include('podiobooks.ratings.urls')),

             # Search
             (r'^search/', include('podiobooks.search.urls')),

             # MUB
             (r'^mub/', include('mub.urls')),
             url(r'^queue/test/$', 'podiobooks.views.test_task_queue', name='test_task_queue'),

             # Robots, Favicon and Related
             (r'^robots\.txt$', vary_on_headers('HOST')(RobotsView.as_view())),
             (r'^favicon\.ico$', AccelView.as_view(url='images/favicon.ico')),
             (r'^apple-touch-icon\.png$',
              AccelView.as_view(url=settings.STATIC_URL + 'images/apple-touch-icon.png')),
             (r'^humans\.txt$', TextTemplateView.as_view(template_name='humans.txt')),
             (r'^crossdomain\.xml', TextTemplateView.as_view(template_name='crossdomain.xml')),

             # Blog
             (r'^blog(?P<url_remainder>.*)', BlogRedirectView.as_view()),

             # Sitemap
             (r'^sitemap\.xml$', sitemap_urls, {'sitemaps': sitemaps}),

             # PB1 Index Page
             (r'index\.php|index\.html', RedirectView.as_view(url='/')),

             # PB1 Search Redirect
             (r'podiobooks/search\.php', RedirectView.as_view(url='/title/search/', query_string=True)),

             # PB1 Authors Doc
             (r'authors/PBAuthoringGuide+', RedirectView.as_view(
                 url='http://blog.podiobooks.com/wp-content/uploads/2012/09/PBAuthoringGuidev2.0.4.pdf')),

             # PB1 Login Page
             (r'account|login\.php|Xlogin\.php|register\.php',
              RedirectView.as_view(url='http://blog.podiobooks.com/what-happened-to-my-login/')),

             # PB1 Charts Page
             (r'charts\.php',
              RedirectView.as_view(url='http://blog.podiobooks.com/what-happened-to-the-charts/')),

             # PB1 Authors Page
             (r'authors\.php|authors/pbpro\.php', RedirectView.as_view(
                 url='http://blog.podiobooks.com/how-to-get-your-books-listed-on-podiobooks-com/')),

             # PB1 Staff Page
             (r'staff\.php', RedirectView.as_view(url='http://blog.podiobooks.com/podiobooks-staff/')),

             # PB1 About Page
             (r'about\.php',
              RedirectView.as_view(url='http://blog.podiobooks.com/frequently-asked-questions/')),

             # PB1 Donate Page
             (r'donate\.php',
              RedirectView.as_view(url='/donate')),

             # PB1 Spread The Word Page
             (r'spreadtheword\.php',
              RedirectView.as_view(url='http://blog.podiobooks.com/why-you-should-donate/')),

             # PB1 Legal Page
             (r'legal\.php', RedirectView.as_view(
                 url='http://blog.podiobooks.com/privacy-and-legal-speak-in-plain-if-not-ill-formed-english/')),

             # Hack Redirect
             (r'submit', RedirectView.as_view(url='/')),

             # Old Infected Redirect
             (r'infected', RedirectView.as_view(url='/title/infected/')),

             # Author Start Page
             (r'start/?$',
              RedirectView.as_view(url='http://blog.podiobooks.com/how-to-get-your-books-listed-on-podiobooks-com/')),

             # Ad Redirect
             (r'website/?$',
              RedirectView.as_view(url='http://a.strk.ly/7WS9s')),

             # Audible Referral Program
             (r'audible/?$',
              RedirectView.as_view(url='http://www.audibletrial.com/PodiobooksAudible')),
    )

# Only hook up the static and media to run through Django in a dev environment...in prod, handle with web server
if settings.DEBUG:
    urlpatterns += patterns('',
                            url(r'^media/(?P<path>.*)$', dev_static_views, {
                                'document_root': settings.MEDIA_ROOT
                            }),
    )
