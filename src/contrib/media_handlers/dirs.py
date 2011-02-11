import os
import sys

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module

fs_encoding = sys.getfilesystemencoding() or sys.getdefaultencoding()

app_css_dirs = []
app_js_dirs = []

for app in settings.INSTALLED_APPS:
    try:
        mod = import_module(app)
    except ImportError,e:
        raise ImproperlyConfigured('ImportError %s: %s' % (app, e.args[0]))
    css_dir = os.path.join(os.path.dirname(mod.__file__),settings.CSS_EXT)
    if os.path.isdir(css_dir):
        app_css_dirs.append(css_dir.decode(fs_encoding))
        
for app in settings.INSTALLED_APPS:
    try:
        mod = import_module(app)
    except ImportError,e:
        raise ImproperlyConfigured('ImportError %s: %s' % (app, e.args[0]))
    css_dir = os.path.join(os.path.dirname(mod.__file__),settings.JS_EXT)
    if os.path.isdir(css_dir):
        app_js_dirs.append(css_dir.decode(fs_encoding))
