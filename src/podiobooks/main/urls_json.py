from django.conf.urls.defaults import * #@UnusedWildImport
from models import Title
from contrib.django_restapi.model_resource import Collection
from contrib.django_restapi.responder import JSONResponder

# Create a handler for RESTful access to the Title Object
# Info At: http://code.google.com/p/django-rest-interface/wiki/RestifyDjango
# @TODO: Consider Piston Framework instead for API layer
title_resource = Collection(
    queryset = Title.objects.all(),
    permitted_methods = ('GET',),
    responder = JSONResponder()
)

urlpatterns = patterns('',
    
    # title
    url(r'^title/(.*?)/?$', title_resource, name='json_title_detail'),
    url(r'^title/$', title_resource, name='json_title_list'),
    
)