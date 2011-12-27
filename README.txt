PODIOBOOKS.COM 2.0
==================
Last Updated: 20 Jan 2009

Team Lead: Tim White (tim@cyface.com)
Team Lead Emeritus: Chris Miller (chris@podiobooks.com)

License
-------
This software is licensed under a GPL v3.0 license. Please visit http://www.gnu.org/licenses/gpl-3.0-standalone.html for a full reading of the license. A full copy has also been included in this package, in LICENSE.txt.

Contributors
------------
Brant Steen (brant@brantsteen.com)

Purpose
-------

The purpose of the Podiobooks project is to create a platform for distributing media via either direct download or via scheduled, updated RSS feeds. Additionally, there should be a strong community element, allowing consumers to connect with each other and the author.  This software will eventually replace the current PHP-based solution at http://www.podiobooks.com.

Required Packages
-----------------
This software depends on the following libraries being available on the Python Path (e.g. having been easy_installed into the site-packages directory)

# Main
django  # 1.x
psycopg2 # 2.x - PostgreSQL driver for Python.  Windows version: http://www.stickpeople.com/projects/python/win-psycopg/
PIL - Python Imaging Library is required to support the ImageFields in the model (requires .exe installer on Windows)

# Admin Site Documentation
docutils # .5

# For Auth OpenID:
python-openid       # http://openidenabled.com/python-openid/   version 2.x
django-authopenid   # http://bitbucket.org/benoitc/django-authopenid
django-registration # http://bitbucket.org/ubernostrum/django-registration/
httplib2 			# http://code.google.com/p/httplib2

# Search:
django-sphinx 2.2.1 # http://github.com/dcramer/django-sphinx (do a git clone of the latest)
Sphinx # Not python, standalone daemon - http://sphinxsearch.com - make sure you compile --with-pgsql or download the binary with PostgreSQL support baked in.

# Cache:
memcached # Not python, standalone daemon - http://www.danga.com/memcached/

# WYSIWYG HTML Editor Integration
django-tinymce # http://code.google.com/p/django-tinymce/
#
