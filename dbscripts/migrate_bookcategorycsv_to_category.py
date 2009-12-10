"""
This script reads in an "CSV for Excel" export from phpMyAdmin into a the new Podiobooks Schema

##############################################
#######-----Book Category Importer----########
##############################################
"""

import csv # first we need import necessary lib:csv
from podiobooks.main.models import *
from django.template.defaultfilters import slugify

def importBookCategories():
    # Now, begin reading in the CSV and using the Django model objects to populate the DB
    
    #Open Category File for Import
    categoryCSVFile=open("podiobooks_legacy_bookcategory_table.csv") #prepare a csv file for our example
    
    #Parse the Category File CSV into a dictionary based on the first row values
    categoryCSVReader=csv.DictReader(categoryCSVFile,dialect='excel')
    
    #Pull off the first row of the book file as the labels
    #categoryLabelRow = categoryCSVReader.next()
    #print categoryLabelRow
    
    #PRE CLEANOUT
    Category.objects.all().delete()
    
    # Loop through the rest of the rows in the CSV
    for row in categoryCSVReader:
        print row
        
        # Create an object in the database based on the current row
        category = Category.objects.create (
            id = row['ID'],
            name = row['Name'].replace('\\',''),
            slug = slugify(row['Name']),
            deleted = False,
        )
        print "Category: %s" % (category.name)
    
    categoryCSVFile.close()

##### MAIN FUNCITON TO RUN IF THIS SCRIPT IS CALLED ALONE ###
if __name__ == "__main__":
    importBookCategories()
    
    
# HANDY MAPPING REFERENCE
# TITLE MODEL FIELDS
#slug = models.SlugField()
#name = models.CharField(max_length=255)
## Note - titles are available as title_set.all()
#deleted = models.BooleanField(default=False)
#date_created = models.DateTimeField(blank=False, default=datetime.datetime.now())
#date_updated = models.DateTimeField(blank=False, default=datetime.datetime.now())

# BOOK CSV FIELDS
#"ID",
#"Name",
#"ParentCatID",
#"Display",#
#"ITunesXML"