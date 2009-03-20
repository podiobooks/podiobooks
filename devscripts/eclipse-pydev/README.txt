This directory contains Eclipse Launch files and eclipse project/path files for use with the Eclipse IDE.

You must have the PyDev extensions for Eclipse installed to use these files.

If you create a new PyDev project, and then pull the code from GitHub into the src directory, you end up with a structure like this:

podiobooks/
	src/
		podiobooks/
			...
			devscripts
			pbsite
			...
			
			
If you do Run->Run Configurations, you should see various podiobooks options, including runserver, which will start the development server on port 8000.

			