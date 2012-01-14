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

The purpose of the Podiobooks project is to create a platform for distributing serialized audiobooks. Additionally, there should be a strong community element, allowing consumers to connect with each other and the author.  This software will eventually replace the current PHP-based solution at http://www.podiobooks.com.

Required Packages
-----------------
This software depends on the following libraries being available on the Python Path (e.g. having been easy_installed into the site-packages directory)

The project has been set up to use Python pip and virtualenv, so you can find an list of all dependencies in the podiobooks/requirements.txt file.

You can choose to install that list of dependencies directly in your Python installation, or using virtualenv.

For development use, a requirements_dev.txt exists to pull in additional packages useful for testing and debugging.

In the devscripts/virtualenv folder are a series of scripts that will be useful in setting up your local development environment with virtualenv, which creates an isolated Python environment just for this project.

A warning that getting the "PIL" imaging library to install correctly using any method is tricky, the easiest way on windows seems to be to install the free Visual Studio Express so that PIP can be compiled.

