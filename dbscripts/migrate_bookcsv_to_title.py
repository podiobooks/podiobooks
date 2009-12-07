"""
This script reads in an "CSV for Excel" export from phpMyAdmin into a the new Podiobooks Schema

##############################################
#######-----Book/Title Importer-------########
##############################################
"""

import csv # first we need import necessary lib:csv
from podiobooks.main.models import *
from django.template.defaultfilters import slugify

#Book/Title Helper Functions

def determineLicense(licenseSlug):
    """Function to look up the license object to attach to the Title"""
    try:
        license = License.objects.get(slug=licenseSlug)
    except:
        if (licenseSlug[:2] == 'by'):
            license = License.objects.create(slug=licenseSlug)
        else:
            license = None
    
    return license

###### Define general utility functions ##########
def booleanClean(data):
    """Function to check fields that we need to convert to boolean"""
    if (data == None) or (data == ''):
        return 0
    else:
        return int(data)

def getOrCreateContributor(contributorName):
    contributorName = contributorName.strip().replace('  ',' ').replace('\\','').replace('&apos;','\'').replace('Theater','Theatre')
    try:
        firstNameGuess, lastNameGuess = contributorName.split(" ")[:2]
    except:
        firstNameGuess = ""
        lastNameGuess = contributorName
        
    contributor, created = Contributor.objects.get_or_create(display_name__iexact=contributorName,
                  defaults={'display_name':contributorName, 'slug': slugify(contributorName), 'first_name': firstNameGuess, 'last_name': lastNameGuess})
    return contributor

def getOrCreateContributorType(contributorType):
    contributorType, created = ContributorType.objects.get_or_create(slug='author',
                  defaults={'name': 'Author',})
    return contributorType

def getCategory(categoryID):
    try:
        category = Category.objects.get(id=categoryID)
    except:
        category = None
    
    return category

def importBooks():
    # Now, begin reading in the CSV and using the Django model objects to populate the DB
    
    #Open Book File for Import
    bookCSVFile=open("podiobooks_legacy_book_table.csv") #prepare a csv file for our example
    
    #Parse the Book File CSV into a dictionary based on the first row values
    bookCSVReader=csv.DictReader(bookCSVFile,dialect='excel')
    
    #PRE CLEANOUT
    Title.objects.all().delete()
    TitleContributors.objects.all().delete()
    Contributor.objects.all().delete()
    
    # Loop through the rest of the rows in the CSV
    for row in bookCSVReader:
        #print row
        
        # Create a title object in the database based on the current book row
        title = Title.objects.create (
            id = row['ID'],
            old_id = row['ID'],
            name = row['Title'].replace('\\',''),
            slug = slugify(row['Title']),
            license = determineLicense(row['license']),
            description = row['Description'].replace('\\',''),
            cover = row['Coverimage'],
            status = 1,
            display_on_homepage = booleanClean(row['DisplayOnHomepage']),
            is_hosted_at_pb = True,
            is_adult = booleanClean(row['Explicit']),
            is_complete = booleanClean(row['Complete']),
            avg_audio_quality = row['AvgAudioQuality'],
            avg_narration = row['AvgNarration'],
            avg_writing = row['AvgWriting'],
            avg_overall = row['AvgOverall'],
            deleted = False,
            date_created = row['DateCreated']
        )
        mainContributor = getOrCreateContributor(row['Authors'][:48])
        contributorType = getOrCreateContributorType('Author')
        TitleContributors.objects.create(title=title,contributor=mainContributor,contributor_type=contributorType)
        category = getCategory(row['CategoryID'])
        if (category):
            title.categories.add(category)
        print "Title: %s\tContributors: %s" % (title.name, title.contributors.values('display_name'))
        title.save()
        
        # Create URL Objects for the URL Fields from the Book Row
        # @TODO Need to double check what we want to do with iTunes, etc.
        
        # Create Media Objects for the URL Fields from the Book Row
        # @TODO Need to double check what we want to do with iTunes, etc.
    
    bookCSVFile.close()

##### MAIN FUNCITON TO RUN IF THIS SCRIPT IS CALLED ALONE ###
if __name__ == "__main__":
    importBooks()
    
    
# HANDY MAPPING REFERENCE
# TITLE MODEL FIELDS
#name = models.CharField(max_length=255)
#series = models.ForeignKey('Series', null=True, blank=True)
#description = models.TextField()
#slug = models.SlugField(max_length=255)
#cover = models.ImageField(upload_to=podiobooks.settings.MEDIA_COVERS)
#status = models.IntegerField(default=1)
#license = models.ForeignKey('License', null=True, blank=True)
#display_on_homepage = models.BooleanField(default=False)
#is_hosted_at_pb = models.BooleanField(default=True)
#advisory = models.ForeignKey('Advisory', null=True, blank=True)
#is_adult = models.BooleanField(default=False)
#is_complete = models.BooleanField(default=False)
#avg_audio_quality = models.FloatField(default=0)
#avg_narration = models.FloatField(default=0)
#avg_writing = models.FloatField(default=0)
#avg_overall = models.FloatField(default=0)
#deleted = models.BooleanField(default=False)
#old_id = models.IntegerField(blank=True, null=True)
#contributors = models.ManyToManyField('Contributor', through='TitleContributors')
#categories = models.ManyToManyField('Category', db_table="main_title_categories")
#awards = models.ManyToManyField('Award', blank=True)
## Note: episodes are available as episode_set.all()
#date_created = models.DateTimeField(blank=False, default=datetime.datetime.now())
#date_updated = models.DateTimeField(blank=False, default=datetime.datetime.now())

# BOOK CSV FIELDS
#"ID"
#"Title"
#"DateCreated"
#"Enabled"
#"AvgRating"
#"Description"
#"Authors"
#"Webpage"
#"FeedURL"
#"UserID"
#"Coverimage"
#"DisplayOnHomepage"
#"CategoryID"
#"Explicit"
#"Subtitle"
#"Standby"
#"Complete"
#"DiscussURL"
#"Notes"
#"BookISBN"
#"AudioISBN"
#"ITunesLink"
#"EBookLink"
#"LuluLink"
#"PartnerID"
#"DynamicAds"
#"AvgAudioQuality"
#"AvgNarration"
#"AvgWriting"
#"AvgOverall"
#"license"
#"itunescategory"
#"FullLocation"
#"FullLength"
#"FullPrice"