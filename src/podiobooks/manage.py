"""Script to wrap the django-admin.py with appropriate settings."""

#!/usr/bin/env python

from django.core.management import execute_manager # pylint: disable-msg=F0401
try:
    import settings # Assumed to be in the same directory. # pylint: disable-msg=W0403
except ImportError:
    import sys
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
    sys.exit(1)

if __name__ == "__main__":
    execute_manager(settings)
