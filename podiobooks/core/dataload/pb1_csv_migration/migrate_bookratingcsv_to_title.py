"""
This script reads in an "CSV for Excel" export from phpMyAdmin into a the new Podiobooks Schema

##############################################
#####-------Book Rating Importer-------#######
##############################################
"""

# pylint: disable=E0611,F0401,W0401,W0614

import csv # first we need import necessary lib:csv
from podiobooks.core.models import *
from django.template.defaultfilters import slugify
from django.core.exceptions import ObjectDoesNotExist

#Define functions for use in importing ratings
def get_title(pb1_book_id):
    """Returns a Title object based on a Legacy Book ID"""
    try:
        found_title = Title.objects.get(id=pb1_book_id)
    except:
        found_title = None
    return found_title

def import_ratings_from_csv():
    """Loops through the chapter rows in the CSV and increment promoter/detractor counts from them"""
    
    #Open Chapter File for Import
    rating_csv_file = open(settings.DATALOAD_DIR + "podiobooks_legacy_bookrating_table.csv")
    
    #Parse the Ratings CSV into a dictionary based on the first row values
    rating_csv_reader = csv.DictReader(rating_csv_file, dialect='excel')
    
    #PRE CLEANOUT
    Title.objects.all().update(promoter_count=0, detractor_count=0)
    
    create_ratings_from_rows(rating_csv_reader)

def create_ratings_from_rows(ratings_list):
   
    # Loop through the rest of the rows in the CSV
    print "Starting Ratings Load:"
    for row in ratings_list:
        found_title = get_title(row['BookID'])
        
        if (found_title != None):
            # Update the title object in the database based on the current rating row
            if float(row['Overall']) >= 3.0:
                found_title.promoter_count = found_title.promoter_count + 1
            else:
                found_title.detractor_count = found_title.detractor_count + 1
            found_title.save()
            
        else:
            "Could not find TitleID#%s" % row['BookID']
            
        try:
            last_rating = Rating.objects.latest()
        except ObjectDoesNotExist:
            last_rating = Rating()
        
        if (last_rating.last_rating_id < int(row['RatingID'])):
            last_rating.last_rating_id = int(row['RatingID'])
            last_rating.date_created = row['DateCreated']
            last_rating.save()
            
    print "All ratings loaded."
        
    
##### MAIN FUNCTION TO RUN IF THIS SCRIPT IS CALLED ALONE ###
if __name__ == "__main__":
    import_ratings_from_csv()


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
