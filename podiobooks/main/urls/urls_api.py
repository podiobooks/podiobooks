from django.conf.urls.defaults import *
from tastypie.api import Api
from podiobooks.main.api import TitleResource

v1_api = Api(api_name='v1')
v1_api.register(TitleResource())

urlpatterns = patterns('',
    (r'', include(v1_api.urls)), #http://localhost:8001/api/v1/title/?format=json
)