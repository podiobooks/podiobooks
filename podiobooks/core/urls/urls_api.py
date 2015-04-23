from django.conf.urls import patterns, include
from podiobooks.core.api import router
 		 
urlpatterns = patterns('',
                  (r'', include(router.urls)),  # http://podiobooks.com/api/titles/
                   ) 		
