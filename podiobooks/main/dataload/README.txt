###
  PODIOBOOKS DATABASE SCRIPTS README
###

The data from the production site, including books, episodes, etc. is loaded using the scripts in this directory.

There is a separate (private) project called podiobooks-dataload that has CSV extracts of the production data that these scripts use.

If you need access to this project, let the team lead know.

The main script is:

	migrate_allcsv_through_model.py

This fires off all the other scripts to CLEAN OUT and load the database fresh from the CSV files.

Note again that it CLEANS OUT the tables it's loading. As in TRUNCATE.


## TRANSLATION SCRIPTS

You will see scripts in this directory called 'xxx_translation.py'.  These scripts do very specific
data cleanup tasks on the PB1 data, to try and fit it better into the PB2 data structures.

They do things like fix author names, assign awards to books, books to series, etc.

All the scripts in this directory exist so that the PB1 data can be pulled into the PB2 datastructures
over and over again, even as the PB2 structures evolve, and without having to have access to the PB1 database.

So, if you see a typo on the PB1 site, you could add a translation to fix it in these scripts.


### GETTING FRESH DATA FROM THE PB1 SITE

There are also scripts in here to pull data directly from the PB1 database.

To use them, you will have to set up a 'pb1prod' datasource in your settings_local.py.

If you need the creds/info for that datasource, email the team lead.


Once you've loaded the base data from the CSVs, you can load the latest data from the production PB1 site via:

	update_from_pb1_data.py

You'll need to set up a PB1 datasource in your settings_local to do this, 

I discourage you from running that without first loading the pre-extracted CSV's (via migrate_allcsv above)...it will take longer and is a heavier load on the PB1 database.

If you need to generate a fresh set of extract CSV's for the podiobooks-dataload project:

	extract_pb1_data_as_csv.py
	
Is the script you want.  It will OVERWRITE the existing CSV extracts in that project.

This script probably doesn't need to get run that often.
