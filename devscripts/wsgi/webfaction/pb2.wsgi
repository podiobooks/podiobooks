import os
import sys

sys.path = ['/home/<username>/webapps/pb2', '/home/<username>/webapps/pb2/pb2', '/home/<username>/webapps/pb2/lib/python2.5', '/home/<username>/webapps/pb2/lib/python2.5/'] + sys.path
from django.core.handlers.wsgi import WSGIHandler

os.environ['DJANGO_SETTINGS_MODULE'] = 'pbsite.settings'
application = WSGIHandler()
