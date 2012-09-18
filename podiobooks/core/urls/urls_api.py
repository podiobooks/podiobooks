from django.conf.urls import patterns, include
from tastypie.api import Api
from podiobooks.core.api import TitleResource

v1_api = Api(api_name='v1')
v1_api.register(TitleResource())

urlpatterns = patterns('',
    (r'', include(v1_api.urls)), #http://podiobooks.com/api/v1/title/?format=json
)