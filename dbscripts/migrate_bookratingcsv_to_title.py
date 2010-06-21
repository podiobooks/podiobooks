"""
This script reads in an "CSV for Excel" export from phpMyAdmin into a the new Podiobooks Schema

##############################################
#####-------Book Rating Importer-------#######
##############################################
"""

import csv # first we need import necessary lib:csv
from podiobooks.main.models import *
from django.template.defaultfilters import slugify

#Define functions for use in importing ratings
def getTitle(legacyBookID):
    """Returns a Title object based on a Legacy Book ID"""
    try:
        foundTitle = Title.objects.get(id=legacyBookID)
    except:
        foundTitle = None
    return foundTitle

def importRatingsFromCSV():
    """Loops through the chapter rows in the CSV and increment promoter/detractor counts from them"""
    
    #Open Chapter File for Import
    ratingCSVFile = open(settings.DATALOAD_DIR + "podiobooks_legacy_bookrating_table.csv")
    
    #Parse the Ratings CSV into a dictionary based on the first row values
    ratingCSVReader = csv.DictReader(ratingCSVFile, dialect='excel')
    
    #PRE CLEANOUT
    Title.objects.all().update(promoter_count=0, detractor_count=0)

def createRatingsFromRows(ratingsList):
   
    # Loop through the rest of the rows in the CSV
    for row in ratingsList:
        foundTitle = getTitle(row['BookID'])
        
        if (foundTitle != None):
            # Update the title object in the database based on the current rating row
            if float(row['Overall']) >= 3.0:
                foundTitle.promoter_count = foundTitle.promoter_count + 1
            else:
                foundTitle.detractor_count = foundTitle.detractor_count + 1
            foundTitle.save()
            
        else:
            "Could not find TitleID#%s" % row['BookID']
            
        try:
            lastRating = Rating.objects.latest('date_created')
        except:
            lastRating = Rating()
            
        lastRating.id = row['RatingID']
        lastRating.date_created = row['DateCreated']
        lastRating.save()
    
##### MAIN FUNCTION TO RUN IF THIS SCRIPT IS CALLED ALONE ###
if __name__ == "__main__":
    importRatingsFromCSV()


# Handy Mapping Reference:
#MODEL FIELDS
#promoter_count = models.IntegerField(default=0)
#detractor_count = models.IntegerField(default=0)

#CSV FIELDS
#RatingID
#BookID
#AudioQuality
#Narration
#Writing
#Overall
#UserID
#DateCreated
#DateModified
