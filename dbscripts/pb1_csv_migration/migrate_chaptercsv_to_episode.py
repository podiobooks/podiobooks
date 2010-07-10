"""
This script reads in an "CSV for Excel" export from phpMyAdmin into a the new Podiobooks Schema

##############################################
#####-----Chapter/Episode Importer-----#######
##############################################
"""

import csv # first we need import necessary lib:csv
from podiobooks.main.models import *
from django.template.defaultfilters import slugify
from podiobooks.libsyn import libsyn_utils
import pprint

#Define functions for use in importing chapters
def getTitle(legacyBookID):
    """Returns a Title object based on a Legacy Book ID"""
    try:
        foundTitle = Title.objects.get(id=legacyBookID)
    except:
        foundTitle = None
    return foundTitle

def importChaptersFromCSV():
    """Loops through the chapter rows in the CSV and build Episode objects for them"""
    
    #Open Chapter File for Import
    chapterCSVFile = open(settings.DATALOAD_DIR + "podiobooks_legacy_chapter_table.csv")
    
    #Parse the Chapter File CSV into a dictionary based on the first row values
    chapterCSVReader = csv.DictReader(chapterCSVFile, dialect='excel')
    
    #PRE CLEANOUT
    Episode.objects.all().delete()
    
    createEpisodesFromRows(chapterCSVReader)

def createEpisodesFromRows(chapterList):
  
    # Loop through the rows
    for row in chapterList:
        foundTitle = getTitle(row['BookID'])
        
        if (foundTitle != None):
            print "Found Title %s" % foundTitle.slug
            # Create an episode object in the database based on the current chapter row
            episode = Episode.objects.create (
                id=row['ID'],
                name=row['Title'].replace('\\', ''),
                title=foundTitle,
                sequence=row['Sequence'],
                description=row['ShowNotes'].replace('\\', '').replace('&#224;', 'a'),
                url=row['Filename'],
                filesize=row['Length'],
                length=0,
                status=1,
                deleted=False,
                date_created=row['DateCreated'],
                date_updated=row['DateUpdated']
            )
            print "episode:",
            print episode.name,
            print ": ",
            print episode.title.slug
            if not episode.title.libsyn_show_id and episode.url:
                print "URL: " + episode.url
                urlTokens = episode.url.split("/")
                host, libsynSlug = urlTokens[2:4]
                if host == 'media.podiobooks.com' and libsynSlug:
                    show_info = libsyn_utils.get_show_info(libsynSlug)
                    if show_info:
                        episode.title.libsyn_show_id = show_info['show_id']
                        episode.title.save()
                        print "LibsynShowId:" + episode.title.libsyn_show_id
        else:
            "Could not find TitleID#%s" % row['BookID']
    
##### MAIN FUNCTION TO RUN IF THIS SCRIPT IS CALLED ALONE ###
if __name__ == "__main__":
    importChaptersFromCSV()


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
