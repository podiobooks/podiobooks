"""
    Master URL Pattern List for the application.  Most of the patterns here should be top-level
    pass-offs to sub-modules, who will have their own urls.py defining actions within.
"""

# pylint: disable=E1120

from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import login as login_view
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.admindocs import urls as admindocs_urls
from django.contrib.sitemaps.views import sitemap as sitemap_urls
from django.views.static import serve as dev_static_views
from django.conf import settings
from django.views.generic import RedirectView
from django.views.decorators.vary import vary_on_headers

from podiobooks.core.sitemaps import AwardDetailSitemap, CategoryDetailSitemap, ContributorDetailSitemap, TitleDetailSitemap
from podiobooks.core.views import IndexView, DonationView, ReportsView, NoMediaReportView

from .views import AccelView, BlogRedirectView, TextTemplateView, RobotsView, test_task_queue

sitemaps = {'AwardDetail': AwardDetailSitemap, 'CategoryDetail': CategoryDetailSitemap,
            'ContributorDetail': ContributorDetailSitemap, 'TitleDetail': TitleDetailSitemap,}

urlpatterns = (
    # Home Page
    url(r'^$', IndexView.as_view(), name="home_page"),

    # Donation Options View
    url(r'^donate/$', DonationView.as_view(), name='donate'),

    # Recent Titles Feed Redirect
    url(r'^index\.xml$', RedirectView.as_view(url='/rss/feeds/titles/recent/', permanent=True)),

    # URLs from core package
    url(r'^', include('podiobooks.core.urls')),

    # Admin documentation
    url(r'^admin/doc/', include(admindocs_urls)),

    # Admin reports
    url(r'^admin/reports/$', staff_member_required(ReportsView.as_view()), name='report_list'),
    url(r'^admin/reports/nomedia/$', staff_member_required(NoMediaReportView.as_view()),
        name='report_nomedia'),

    # Admin Site
    url(r'^admin/', include(admin.site.urls)),

    # Auth / Login
    url(r'^account/signin/$', login_view),

    # Feeds
    url(r'^rss/', include('podiobooks.feeds.urls')),

    # FireTv
    url(r'^firetv/', include('podiobooks.firetv.urls')),

    # Libsyn Utils
    url(r'^libsyn/', include('podiobooks.libsyn.urls')),

    # Ratings
    url(r'^rate/', include('podiobooks.ratings.urls')),

    # Search
    url(r'^search/', include('podiobooks.search.urls')),

    # MUB
    url(r'^mub/', include('mub.urls')),
    url(r'^queue/test/$', test_task_queue, name='test_task_queue'),

    # Robots, Favicon and Related
    url(r'^robots\.txt$', vary_on_headers('HOST')(RobotsView.as_view())),
    url(r'^favicon\.ico$', AccelView.as_view(url='images/favicon.ico')),
    url(r'^apple-touch-icon\.png$', AccelView.as_view(url=settings.STATIC_URL + 'images/apple-touch-icon.png')),
    url(r'^humans\.txt$', TextTemplateView.as_view(template_name='humans.txt')),
    url(r'^crossdomain\.xml', TextTemplateView.as_view(template_name='crossdomain.xml')),

    # Blog
    url(r'^blog(?P<url_remainder>.*)', BlogRedirectView.as_view()),

    # Sitemap
    url(r'^sitemap\.xml$', sitemap_urls, {'sitemaps': sitemaps}),

    # PB1 Index Page
    url(r'index\.php|index\.html', RedirectView.as_view(url='/', permanent=True)),

    # PB1 Search Redirect
    url(r'podiobooks/search\.php', RedirectView.as_view(url='/title/search/', permanent=True, query_string=True)),

    # PB1 Authors Doc
    url(r'authors/PBAuthoringGuide+', RedirectView.as_view(url='http://blog.podiobooks.com/wp-content/uploads/2012/09/PBAuthoringGuidev2.0.4.pdf', permanent=True)),

    # PB1 Login Page
    url(r'account|login\.php|Xlogin\.php|register\.php', RedirectView.as_view(url='http://blog.podiobooks.com/what-happened-to-my-login/', permanent=True)),

    # PB1 Charts Page
    url(r'charts\.php', RedirectView.as_view(url='http://blog.podiobooks.com/what-happened-to-the-charts/', permanent=True)),

    # PB1 Authors Page
    url(r'authors\.php|authors/pbpro\.php', RedirectView.as_view(url='http://blog.podiobooks.com/how-to-get-your-books-listed-on-podiobooks-com/', permanent=True)),

    # PB1 Staff Page
    url(r'staff\.php', RedirectView.as_view(url='http://blog.podiobooks.com/podiobooks-staff/', permanent=True)),

    # PB1 About Page
    url(r'about\.php', RedirectView.as_view(url='http://blog.podiobooks.com/frequently-asked-questions/', permanent=True)),

    # PB1 Donate Page
    url(r'donate\.php', RedirectView.as_view(url='/donate', permanent=True)),

    # PB1 Spread The Word Page
    url(r'spreadtheword\.php', RedirectView.as_view(url='http://blog.podiobooks.com/why-you-should-donate/', permanent=True)),

    # PB1 Legal Page
    url(r'legal\.php', RedirectView.as_view(url='http://blog.podiobooks.com/privacy-and-legal-speak-in-plain-if-not-ill-formed-english/', permanent=True)),

    # Hack Redirect
    url(r'submit', RedirectView.as_view(url='/', permanent=True)),

    # Old Infected Redirect
    url(r'infected', RedirectView.as_view(url='/title/infected/', permanent=True)),

    # Author Start Page
    url(r'start/?$', RedirectView.as_view(url='http://blog.podiobooks.com/how-to-get-your-books-listed-on-podiobooks-com/', permanent=True)),

    # Ad Redirect
    url(r'website/?$', RedirectView.as_view(url='http://a.strk.ly/7WS9s', permanent=True)),

    # Audible Referral Program
    url(r'audible/?$', RedirectView.as_view(url='http://www.audibletrial.com/PodiobooksAudible', permanent=True)),

    # Audiobooks Referral Program
    url(r'audiobooks/?$', RedirectView.as_view(url='http://affiliates.audiobooks.com/tracking/scripts/click.php?a_aid=54cb451d1bf77&a_bid=52ce997a', permanent=True)),

    # Pledge Vanity URL
    url(r'pledge/?$', RedirectView.as_view(url='https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=H32A88G62SBKQ', permanent=True)),
)

# Only hook up the static and media to run through Django in a dev environment...in prod, handle with web server
if settings.DEBUG:
    urlpatterns += (
        url(r'^media/(?P<path>.*)$', dev_static_views, {
            'document_root': settings.MEDIA_ROOT
        }),
    )
    import debug_toolbar

    urlpatterns += (
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
