"""
This script reads in an "CSV for Excel" export from phpMyAdmin into a the new Podiobooks Schema

##############################################
#######-----Book/Title Importer-------########
##############################################
"""

import csv # first we need import necessary lib:csv
from podiobooks.main.models import *
from django.template.defaultfilters import slugify
from djangolinks.models import Link
import contributor_translation
import award_translation
import series_translation

#Book/Title Helper Functions

def determineLicense(licenseSlug):
    """Function to look up the license object to attach to the Title"""
    try:
        license = License.objects.get(slug=licenseSlug)
    except:
        if licenseSlug[:2] == 'by':
            license = License.objects.create(slug=licenseSlug)
        elif licenseSlug == 'all':
            license = License.objects.create(slug=licenseSlug)
        else:
            license = license = License.objects.get(slug='by-nc-nd')
    
    return license

###### Define general utility functions ##########
def booleanClean(data):
    """Function to check fields that we need to convert to boolean"""
    if (data == None) or (data == ''):
        return 0
    else:
        return int(data)
    
def getOrCreateAward(awardSlug):
    """Retrieves or creates an Award type based on the slug of the award"""

    award, created = Award.objects.get_or_create(slug__iexact=awardSlug,
              defaults={ 'name':awardSlug, 'image': 'unknown', 'url': 'unknown' })
    return award

def getOrCreateContributor(contributorName):
    """Retrieves or creates a Contributor based on the name of the Contributor"""
    contributorName = contributorName.strip().replace('  ',' ').replace('\\','').replace('&apos;','\'').replace('Theater','Theatre').replace('J. C.','J.C.').replace('J. A.','J.A.').replace('J. J.','J.J.').replace('J. T.','J.T.').replace('J. P.','J.P.')
    try:
        contributorNameToSplit = contributorName.replace(' III','')
        contributorNameTokens = contributorNameToSplit.split(" ", 2)
        if (len(contributorNameTokens) > 2):
            firstNameGuess, middleNameGuess, lastNameGuess = contributorNameTokens[:3]
        else:
            firstNameGuess, lastNameGuess = contributorNameTokens[:2]
            middleNameGuess = ""
    except:
        firstNameGuess = ""
        middleNameGuess = ""
        lastNameGuess = contributorName
        
    contributor, created = Contributor.objects.get_or_create(display_name__iexact=contributorName,
                  defaults={ 'display_name':contributorName, 'slug': slugify(contributorName), 'first_name': firstNameGuess, 'middle_name': middleNameGuess.replace(',',''), 'last_name': lastNameGuess.replace(',','') })
    return contributor

def getOrCreateContributorType(contributorType):
    """Retrieves or creates a Contributor type based on the name of the type"""
    contributorTypeObject, created = ContributorType.objects.get_or_create(slug=slugify(contributorType),
                  defaults={'name': contributorType,})
    return contributorTypeObject

def getCategory(categoryID):
    """Retrieves a category by id or none if not found"""
    try:
        category = Category.objects.get(id=categoryID)
    except:
        category = None
    
    return category

def getPartner(partnerID):
    """Retrieves a partner by id or none if not found"""
    try:
        partner = Partner.objects.get(id=partnerID)
    except:
        partner = None
    
    return partner

def getOrCreateSeries(seriesSlug):
    """Retrieves or creates an Series based on the slug of the series"""

    series, created = Series.objects.get_or_create(slug__iexact=seriesSlug,
              defaults={ 'name':seriesSlug, })
    return series

def importBooks():
    """Reads in the CSV and using the Django model objects to populate the DB"""
    
    #Open Book File for Import
    bookCSVFile=open("podiobooks_legacy_book_table.csv")
    
    #Parse the Book File CSV into a dictionary based on the first row values
    bookCSVReader=csv.DictReader(bookCSVFile,dialect='excel')
    
    #PRE CLEANOUT
    Title.objects.all().delete()
    TitleContributors.objects.all().delete()
    Contributor.objects.all().delete()
    
    # Loop through the rest of the rows in the CSV
    for row in bookCSVReader:
        #print row
        
        if (int(row['Enabled']) == 1 and int(row['Standby']) == 0):
            # Create a title object in the database based on the current book row
            title = Title.objects.create (
                id = row['ID'],
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
                podiobooker_blog_url = row['DiscussURL'],
                date_created = row['DateCreated']
            )
            
            """ Contributors """
            contributorList = contributor_translation.translate_contributor(row['Authors']) #Manual Contributor Lookup Translation
            for contributor in contributorList:
                contributorObject = getOrCreateContributor(contributor['name'])
                contributorType = getOrCreateContributorType(contributor['type'])
                TitleContributors.objects.create(title=title,contributor=contributorObject,contributor_type=contributorType)
            print "Title: %s\tContributors: %s" % (title.name, title.contributors.values('display_name'))
            
            """ Awards """
            awardList = award_translation.translate_award(row['ID']) #Manual Award Lookup Translation
            if awardList:
                for awardSlug in awardList:
                    awardObject = getOrCreateAward(awardSlug)
                    title.awards.add(awardObject)
                print "Title: %s\tAwards: %s" % (title.name, title.awards.values('name'))
            
            """ Series """
            seriesSlug = series_translation.translate_series(row['ID']) #Manual Series Lookup Translation
            if seriesSlug:
                seriesObject = getOrCreateSeries(seriesSlug)
                title.series = seriesObject
                print "Title: %s\tSeries: %s" % (title.name, title.series.name)
            
            """ Category """
            category = getCategory(row['CategoryID'])
            if category:
                title.categories.add(category)
                print "Title: %s\tCategories: %s" % (title.name, title.categories.values('name'))
            
            """ Partner """
            partner = getPartner(row['PartnerID'])
            if partner:
                title.partner = partner
                print "Title: %s\tPartner: %s" % (title.name, title.partner.name)
                
            title.save()
            
        # @TODO Need to double check what we want to do with URLs to iTunes, etc.
        
        # @TODO Create Media Objects for the URL Fields from the Book Row
    
    bookCSVFile.close()

##### MAIN FUNCTION TO RUN IF THIS SCRIPT IS CALLED ALONE ###
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
#contributors = models.ManyToManyField('Contributor', through='TitleContributors')
#categories = models.ManyToManyField('Category', db_table="main_title_categories")
#awards = models.ManyToManyField('Award', blank=True)
## Note: episodes are available as episode_set.all()
#date_created = models.DateTimeField(blank=False, default=datetime.datetime.now())
#date_updated = models.DateTimeField(blank=False, default=datetime.datetime.now())

# BOOK CSV FIELDS
#"ID" /
#"Title"/
#"DateCreated" /
#"Enabled" /
#"AvgRating"
#"Description" /
#"Authors" /
#"Webpage"
#"FeedURL"
#"UserID"
#"Coverimage" /
#"DisplayOnHomepage" /
#"CategoryID" /
#"Explicit" /
#"Subtitle"
#"Standby"
#"Complete" /
#"DiscussURL"
#"Notes"
#"BookISBN"
#"AudioISBN"
#"ITunesLink"
#"EBookLink"
#"LuluLink"
#"PartnerID" /
#"DynamicAds"
#"AvgAudioQuality" /
#"AvgNarration" /
#"AvgWriting" /
#"AvgOverall" /
#"license"
#"itunescategory"
#"FullLocation"
#"FullLength"
#"FullPrice"