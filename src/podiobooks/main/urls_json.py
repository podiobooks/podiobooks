"""Define a set of URLS that return JSON from REST-style Calls"""

# pylint: disable-msg=W0401,W0614

from django.conf.urls.defaults import * #@UnusedWildImport
from podiobooks.main.models import Title, Category, Contributor
from contrib.django_restapi.model_resource import Collection
from contrib.django_restapi.responder import JSONResponder

# Create a handler for RESTful access to the Title Object
# Info At: http://code.google.com/p/django-rest-interface/wiki/RestifyDjango
# @TODO: Consider Piston Framework instead for API layer
TITLE_RESOURCE = Collection(
    queryset=Title.objects.all(),
    permitted_methods=('GET',),
    responder=JSONResponder()
)

CATEGORY_RESOURCE = Collection(
    queryset=Category.objects.all(),
    permitted_methods=('GET',),
    responder=JSONResponder()
)

CONTRIBUTOR_RESOURCE = Collection(
    queryset=Contributor.objects.all(),
    permitted_methods=('GET',),
    responder=JSONResponder()
)

urlpatterns = patterns('',
    
    # title
    url(r'^title/(.*?)/?$', TITLE_RESOURCE, name='json_title_detail'),
    url(r'^title/$', TITLE_RESOURCE, name='json_title_list'),
    url(r'^categories/$', CATEGORY_RESOURCE, name='json_category_list'),
    url(r'^contributors/$', CONTRIBUTOR_RESOURCE, name='json_contributor_list'),
    
)
