"""
This script reads in an "CSV for Excel" export from phpMyAdmin into a the new Podiobooks Schema

##############################################
#######-----Book/Title Importer-------########
##############################################
"""

import csv # first we need import necessary lib:csv
from podiobooks.main.models import *
from django.template.defaultfilters import slugify
from data_cleanup import contributor_translation
from data_cleanup import award_translation
from data_cleanup import series_translation

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
        if int(data) >= 1:
            return True
        else:
            return False
    
def getOrCreateAward(awardSlug):
    """Retrieves or creates an Award type based on the slug of the award"""

    award, created = Award.objects.get_or_create(slug__iexact=awardSlug,
              defaults={ 'slug': awardSlug, 'name':awardSlug, 'image': 'unknown', 'url': 'unknown' })
    return award

def getOrCreateContributor(contributorName):
    """Retrieves or creates a Contributor object based on the name of the Contributor"""
    contributorName = contributorName.strip().replace('  ', ' ').replace('\\', '').replace('&apos;', '\'').replace('Theater', 'Theatre').replace('J. C.', 'J.C.').replace('J. A.', 'J.A.').replace('J. J.', 'J.J.').replace('J. T.', 'J.T.').replace('J. P.', 'J.P.').replace('JP', 'J.P.').replace('I G', 'I.G.')
    try:
        contributorNameToSplit = contributorName.replace(' III', '')
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
                  defaults={ 'display_name':contributorName, 'slug': slugify(contributorName), 'first_name': firstNameGuess, 'middle_name': middleNameGuess.replace(',', ''), 'last_name': lastNameGuess.replace(',', '').replace(' Ph.D.', '') })
    return contributor

def getOrCreateContributorType(contributorType):
    """Retrieves or creates a Contributor type based on the name of the type"""
    contributorTypeSlug = slugify(contributorType)
    contributorTypeToBylineMapping = {
      'author': " and ",
      'editor':" edited by ",
      'narrator': " narrated by ",
      'penname': " writing as ",
      'ghostwriter': " as told to ",
      'contributor': " with ",
    }
    byline_text = contributorTypeToBylineMapping[contributorTypeSlug]
    if not byline_text:
        byline_text = ""
    contributorTypeObject, created = ContributorType.objects.get_or_create(slug=contributorTypeSlug,
                  defaults={'name': contributorType, 'byline_text': byline_text })
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
              defaults={ 'slug': seriesSlug, 'name': seriesSlug, })
    return series

def getLibsynIDCache():
    libsynIDCache = {}
    
    #Open Cache File for Import
    cacheCSVFile = open(settings.DATALOAD_DIR + "podiobooks_libsyn_id_cache.csv")
    
    #Parse the Cache File CSV into a dictionary based on the first row values
    cacheCSVReader = csv.DictReader(cacheCSVFile, dialect='excel')
    
    for title in cacheCSVReader:
        libsynIDCache[ title['ID'] ] = title['LibsynShowId']
        
    return libsynIDCache

def getiTunesIDCache():
    iTunesIDCache = {}
    
    #Open Cache File for Import
    cacheCSVFile = open(settings.DATALOAD_DIR + "podiobooks_itunes_id_cache.csv")
    
    #Parse the Cache File CSV into a dictionary based on the first row values
    cacheCSVReader = csv.DictReader(cacheCSVFile, dialect='excel')
    
    for title in cacheCSVReader:
        print title
        if title['ID']:
            iTunesIDCache[ title['ID'] ] = title['iTunesID']
        
        if title['Slug']:
            iTunesIDCache[ title['Slug'] ] = title['iTunesID']
            
    return iTunesIDCache

def importBooksFromCSV():
    """Reads in the CSV and using the Django model objects to populate the DB"""
    
    #Open Book File for Import
    bookCSVFile = open(settings.DATALOAD_DIR + "podiobooks_legacy_book_table.csv")
    
    #Parse the Book File CSV into a dictionary based on the first row values
    bookCSVReader = csv.DictReader(bookCSVFile, dialect='excel')
    
    #PRE CLEANOUT
    Title.objects.all().delete()
    TitleContributor.objects.all().delete()
    Contributor.objects.all().delete()
    
    createTitlesFromRows(bookCSVReader)
 
def createTitlesFromRows(titleList):
    """Takes a list of title rows from a database query or a CSV file read and creates Title objects"""
    
    libsynIDCache = getLibsynIDCache()  #Load the Libsyn ID Cache from its CSV
    iTunesIDCache = getiTunesIDCache()  #Load the iTunes ID Cache from its CSV
    
    # Loop through the rest of the rows in the CSV
    for row in titleList:
        
        # Look up iTunesID in Cache
        iTunesID = None
        try:
            iTunesID = iTunesIDCache[row['ID']]
        except KeyError:
            try:
                iTunesID = iTunesIDCache[row['Subtitle']]
            except KeyError:
                pass
        
        if (int(row['Enabled']) == 1 and int(row['Standby']) == 0):
            # Create a title object in the database based on the current book row
            title = Title.objects.create (
                id=row['ID'],
                name=row['Title'].replace('\\', ''),
                slug=slugify(row['Title']),
                license=determineLicense(row['license']),
                description=row['Description'].replace('\\', ''),
                cover=row['Coverimage'],
                status=1,
                display_on_homepage=booleanClean(row['DisplayOnHomepage']),
                is_hosted_at_pb=True,
                is_explicit=booleanClean(row['Explicit']),
                is_complete=booleanClean(row['Complete']),
                avg_audio_quality=row['AvgAudioQuality'],
                avg_narration=row['AvgNarration'],
                avg_writing=row['AvgWriting'],
                avg_overall=row['AvgOverall'],
                deleted=False,
                podiobooker_blog_url=row['DiscussURL'],
                libsyn_show_id=libsynIDCache.get(row['ID'],""),
                itunes_adam_id=iTunesID,
                date_created=row['DateCreated']
            )
            
            """ Contributors """
            contributorList = contributor_translation.translate_contributor(row['Authors']) #Manual Contributor Lookup Translation
            for contributor in contributorList:
                contributorObject = getOrCreateContributor(contributor['name'])
                contributorType = getOrCreateContributorType(contributor['type'])
                TitleContributor.objects.create(title=title, contributor=contributorObject, contributor_type=contributorType)
            print "Title: %s\n\t\tContributors: %s" % (title.name, title.contributors.values('display_name'))
            
            """ Awards """
            awardList = award_translation.translate_award(row['ID']) #Manual Award Lookup Translation
            if awardList:
                for awardSlug in awardList:
                    awardObject = getOrCreateAward(awardSlug)
                    title.awards.add(awardObject)
                print "\t\tAwards: %s" % (title.awards.values('name'))
            
            """ Series """
            seriesSlug = series_translation.translate_series(row['ID']) #Manual Series Lookup Translation
            if seriesSlug:
                seriesObject = getOrCreateSeries(seriesSlug)
                title.series = seriesObject
                print "\t\tSeries: %s" % (title.series.name)
            
            """ Category """
            category = getCategory(row['CategoryID'])
            if category:
                TitleCategory.objects.create(title=title,category=category)
                print "\t\tCategories: %s" % (title.categories.values('name'))
                if category.slug == 'erotica':
                    title.is_adult = True
            
            """ Partner """
            partner = getPartner(row['PartnerID'])
            if partner:
                title.partner = partner
                print "\t\tPartner: %s" % (title.partner.name)
                
            title.save()
            
        # @TODO Need to double check what we want to do with URLs to iTunes, etc.
        
        # @TODO Create Media Objects for the URL Fields from the Book Row

##### MAIN FUNCTION TO RUN IF THIS SCRIPT IS CALLED ALONE ###
if __name__ == "__main__":
    importBooksFromCSV()
    
    
# HANDY MAPPING REFERENCE
# TITLE MODEL FIELDS
#name = models.CharField(max_length=255)
#series = models.ForeignKey('Series', null=True, blank=True)
#description = models.TextField()
#slug = models.SlugField(max_length=255)
#cover = models.ImageField(upload_to=settings.MEDIA_COVERS)
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
#contributors = models.ManyToManyField('Contributor', through='TitleContributor')
#categories = models.ManyToManyField('Category', db_table="main_title_categories")
#awards = models.ManyToManyField('Award', blank=True)
## Note: episodes are available as episodes.all()
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
