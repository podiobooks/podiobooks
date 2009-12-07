"""
This script reads in an "CSV for Excel" export from phpMyAdmin into a the new Podiobooks Schema

##############################################
#####-----Chapter/Episode Importer-----#######
##############################################
"""

import csv # first we need import necessary lib:csv
from podiobooks.main.models import *
from django.template.defaultfilters import slugify

#Define functions for use in importing chapters
def getTitle(legacyBookID):
    """Returns a Title object based on a Legacy Book ID"""
    try:
        foundTitle = Title.objects.get(old_id=legacyBookID)
    except:
        foundTitle = None
    return foundTitle

def importChapters():
    """Loops through the chapter rows in the CSV and build Episode objects for them"""
    
    #Open Chapter File for Import
    chapterCSVFile=open("podiobooks_legacy_chapter_table.csv") #prepare a csv file for our example
    
    #Parse the Chapter File CSV into a dictionary based on the first row values
    chapterCSVReader=csv.DictReader(chapterCSVFile,dialect='excel')
    
    #PRE CLEANOUT
    Episode.objects.all().delete()
    
    # Loop through the rest of the rows in the CSV
    for row in chapterCSVReader:
        #print row
        
        foundTitle = getTitle(row['BookID'])
        
        if (foundTitle != None):
            print "Found Title %s" % foundTitle.slug
            # Create an episode object in the database based on the current chapter row
            episode = Episode.objects.create (
                id = row['ID'],
                old_id = row['ID'],
                name = row['Title'].replace('\\',''),
                title = foundTitle,
                sequence = row['Sequence'],
                description = row['ShowNotes'].replace('\\',''),
                url = row['Filename'],
                filesize = row['Length'],
                length = 0,
                status = 1,
                deleted = False,
                date_created = row['DateCreated']
            )
            print "episode:",
            print episode.name,
            print ": ",
            print episode.title.slug
        else:
            "Could not find TitleID#%s" % row['BookID']
    
    chapterCSVFile.close()
    
##### MAIN FUNCITON TO RUN IF THIS SCRIPT IS CALLED ALONE ###
if __name__ == "__main__":
    importChapters()


# Handy Mapping Reference:
#MODEL FIELDS
#title = models.ForeignKey('Title')
#name = models.CharField(max_length=255)
#sequence = models.IntegerField(blank=False, null=False)
#description = models.TextField(blank=True)
#url = models.URLField(blank=False, verify_exists=True)
#filesize = models.FloatField(default=0)
#status = models.SmallIntegerField(default=1)
#deleted = models.BooleanField(default=False)
#old_id = models.IntegerField(blank=True, null=True)
#date_created = models.DateTimeField(blank=False, default=datetime.datetime.now())
#date_updated = models.DateTimeField(blank=False, default=datetime.datetime.now())

#CSV FIELDS
#"ID"
#"BookID"
#"Sequence"
#"ShowNotes"
#"Filename"
#"DateCreated"
#"DateUpdated"
#"Enabled"
#"StatusID"
#"Bitrate"
#"Title"
#"Length"
#"Format"
#"NumDownloads"