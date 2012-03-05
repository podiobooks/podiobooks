"""
This script reads in an "CSV for Excel" export from phpMyAdmin into a the new Podiobooks Schema

##############################################
#######--------Partner Importer-------########
##############################################
"""

import csv # first we need import necessary lib:csv
from podiobooks.main.models import *
from django.template.defaultfilters import slugify

def import_partners_from_csv():
    # Now, begin reading in the CSV and using the Django model objects to populate the DB
    
    #Open Partner File for Import
    partnerCSVFile = open(settings.DATALOAD_DIR + "podiobooks_legacy_partner_table.csv")
    
    #Parse the Partner File CSV into a dictionary based on the first row values
    partnerCSVReader = csv.DictReader(partnerCSVFile, dialect='excel')
    
    #PRE CLEANOUT
    Partner.objects.all().delete()
    
    create_partners_from_rows(partnerCSVReader)

def create_partners_from_rows(partnerList):
    # Loop through the rest of the rows in the CSV
    for row in partnerList:
        print row
        
        # Create an object in the database based on the current row
        partner = Partner.objects.create (
            id=row['ID'],
            name=row['Name'].replace('\\', ''),
            url=row['URL'],
            logo=row['Logo'],
            deleted=False,
            date_created=row['datecreated'],
        )
        print "Partner: %s" % (partner.name)

##### MAIN FUNCTION TO RUN IF THIS SCRIPT IS CALLED ALONE ###
if __name__ == "__main__":
    import_partners_from_csv()
    
    
# HANDY MAPPING REFERENCE
# TITLE MODEL FIELDS
#name = models.CharField(blank=False, max_length=255)
#url = models.URLField(blank=False, verify_exists=True)
#logo = models.ImageField(upload_to="/dir/path")
#deleted = models.BooleanField(default=False)
#date_created = models.DateTimeField(blank=False, default=datetime.datetime.now())
#date_updated = models.DateTimeField(blank=False, default=datetime.datetime.now())

# BOOK CSV FIELDS
#"ID",
#"Name",
#"URL",
#"Logo",
#"CSS",
#"HasLibrary",
#"enabled",
#"datecreated",
#"HeaderHTML",
#"FooterHTML"
