"""
This script reads in an "CSV for Excel" export from phpMyAdmin into a the new Podiobooks Schema

##############################################
#####-----Chapter/Episode Importer-----#######
##############################################
"""

# pylint: disable=E0611,F0401,W0401,W0614

import csv # first we need import necessary lib:csv
from podiobooks.core.models import *
from podiobooks.libsyn import libsyn_utils

#Define functions for use in importing chapters
def get_title(pb1_book_id):
    """Returns a Title object based on a Legacy Book ID"""
    try:
        found_title = Title.objects.get(id=pb1_book_id)
    except:
        found_title = None
    return found_title

def import_chapters_from_csv():
    """Loops through the chapter rows in the CSV and build Episode objects for them"""
    
    #Open Chapter File for Import
    chapter_csv_file = open(settings.DATALOAD_DIR + "podiobooks_legacy_chapter_table.csv")
    
    #Parse the Chapter File CSV into a dictionary based on the first row values
    chapter_csv_reader = csv.DictReader(chapter_csv_file, dialect='excel')
    
    #PRE CLEANOUT
    Episode.objects.all().delete()
    
    create_episodes_from_chapter_rows(chapter_csv_reader)

def create_episodes_from_chapter_rows(chapter_list):
    """Create Episode objects from each PB1 Chapter"""
  
    # Loop through the rows
    for row in chapter_list:
        found_title = get_title(row['BookID'])
        
        if (found_title != None):
            print "Found Title %s" % found_title.slug
            # Create an episode object in the database based on the current chapter row
            episode = Episode.objects.create (
                id=row['ID'],
                name=row['Title'].replace('\\', ''),
                title=found_title,
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
            print ("Could not find TitleID#%s" % row['BookID'])
    
##### MAIN FUNCTION TO RUN IF THIS SCRIPT IS CALLED ALONE ###
if __name__ == "__main__":
    import_chapters_from_csv()


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
