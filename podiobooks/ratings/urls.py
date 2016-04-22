"""Django URLs for Ratings"""

from django.conf.urls import url
from .views import RateTitleView
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from podiobooks.ratings.views import get_ratings

urlpatterns = (
    url(r'^(?P<slug>[^/]+)/$', get_ratings, name='get_ratings'),

    # Promote Title
    url(r'^(?P<slug>[^/]+)/promote/$', never_cache(csrf_protect(RateTitleView.as_view())), name='promote_title'),

    # Detract Title
    url(r'^(?P<slug>[^/]+)/detract/$', never_cache(csrf_protect(RateTitleView.as_view())), kwargs={"up_vote": False}, name='detract_title'),
)
