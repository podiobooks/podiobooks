from django.conf.urls.defaults import * #@UnusedWildImport
from models import Title, Category, Contributor
from contrib.django_restapi.model_resource import Collection
from contrib.django_restapi.responder import JSONResponder

# Create a handler for RESTful access to the Title Object
# Info At: http://code.google.com/p/django-rest-interface/wiki/RestifyDjango
# @TODO: Consider Piston Framework instead for API layer
title_resource = Collection(
    queryset=Title.objects.all(),
    permitted_methods=('GET',),
    responder=JSONResponder()
)

category_resource = Collection(
    queryset=Category.objects.all(),
    permitted_methods=('GET',),
    responder=JSONResponder()
)

contributor_resouce = Collection(
    queryset=Contributor.objects.all(),
    permitted_methods=('GET',),
    responder=JSONResponder()
)

urlpatterns = patterns('',
    
    # title
    url(r'^title/(.*?)/?$', title_resource, name='json_title_detail'),
    url(r'^title/$', title_resource, name='json_title_list'),
    url(r'^categories/$', category_resource, name='json_category_list'),
    url(r'^contributors/$', contributor_resouce, name='json_contributor_list'),
    
)
