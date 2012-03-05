"""
This script reads in an "CSV for Excel" export from phpMyAdmin into a the new Podiobooks Schema

##############################################
#######-----Book/Title Importer-------########
##############################################
"""

# pylint: disable=E0611,F0401,W0401,W0614

import csv # first we need import necessary lib:csv
from podiobooks.core.models import *
from django.template.defaultfilters import slugify
from podiobooks.core.dataload.data_cleanup import contributor_translation
from podiobooks.core.dataload.data_cleanup import award_translation
from podiobooks.core.dataload.data_cleanup import series_translation

#Book/Title Helper Functions

def determine_license(license_slug):
    """Function to look up the license object to attach to the Title"""
    try:
        license = License.objects.get(slug=license_slug)
    except:
        if license_slug[:2] == 'by':
            license = License.objects.create(slug=license_slug)
        elif license_slug == 'all':
            license = License.objects.create(slug=license_slug)
        else:
            license = license = License.objects.get(slug='by-nc-nd')
    
    return license

###### Define general utility functions ##########
def boolean_clean(data):
    """Function to check fields that we need to convert to boolean"""
    if (data == None) or (data == ''):
        return 0
    else:
        if int(data) >= 1:
            return True
        else:
            return False
    
def get_or_create_award(award_slug):
    """Retrieves or creates an Award type based on the slug of the award"""

    award, created = Award.objects.get_or_create(slug__iexact=award_slug,
              defaults={ 'slug': award_slug, 'name':award_slug, 'image': 'unknown', 'url': 'unknown' })
    return award

def get_or_create_contributor(contributor_name):
    """Retrieves or creates a Contributor object based on the name of the Contributor"""
    contributor_name = contributor_name.strip().replace('  ', ' ').replace('\\', '').replace('&apos;', '\'').replace('Theater', 'Theatre').replace('J. C.', 'J.C.').replace('J. A.', 'J.A.').replace('J. J.', 'J.J.').replace('J. T.', 'J.T.').replace('J. P.', 'J.P.').replace('JP', 'J.P.').replace('I G', 'I.G.')
    try:
        contributor_name_to_split = contributor_name.replace(' III', '')
        contributor_name_tokens = contributor_name_to_split.split(" ", 2)
        if (len(contributor_name_tokens) > 2):
            first_name_guess, middle_name_guess, last_name_guess = contributor_name_tokens[:3]
        else:
            first_name_guess, last_name_guess = contributor_name_tokens[:2]
            middle_name_guess = ""
    except:
        first_name_guess = ""
        middle_name_guess = ""
        last_name_guess = contributor_name
        
    contributor, created = Contributor.objects.get_or_create(display_name__iexact=contributor_name,
                  defaults={ 'display_name':contributor_name, 'slug': slugify(contributor_name), 'first_name': first_name_guess, 'middle_name': middle_name_guess.replace(',', ''), 'last_name': last_name_guess.replace(',', '').replace(' Ph.D.', '') })
    return contributor

def get_or_create_contributor_type(contributor_type):
    """Retrieves or creates a Contributor type based on the name of the type"""
    contributorTypeSlug = slugify(contributor_type)
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
                  defaults={'name': contributor_type, 'byline_text': byline_text })
    return contributorTypeObject

def get_category(category_id):
    """Retrieves a category by id or none if not found"""
    try:
        category = Category.objects.get(id=category_id)
    except:
        category = None
    
    return category

def get_partner(partner_id):
    """Retrieves a partner by id or none if not found"""
    try:
        partner = Partner.objects.get(id=partner_id)
    except:
        partner = None
    
    return partner

def get_or_create_series(series_slug):
    """Retrieves or creates an Series based on the slug of the series"""

    series, created = Series.objects.get_or_create(slug__iexact=series_slug,
              defaults={ 'slug': series_slug, 'name': series_slug, })
    return series

def get_libsyn_id_cache():
    """Pull up the file containing the cache of libsyn IDs and load it into an object for use"""
    libsynIDCache = {}
    
    #Open Cache File for Import
    cacheCSVFile = open(settings.DATALOAD_DIR + "podiobooks_libsyn_id_cache.csv")
    
    #Parse the Cache File CSV into a dictionary based on the first row values
    cacheCSVReader = csv.DictReader(cacheCSVFile, dialect='excel')
    
    for title in cacheCSVReader:
        libsynIDCache[ title['ID'] ] = title['LibsynShowId']
        
    return libsynIDCache

def get_itunes_id_cache():
    """Pull up the file containing the cache of itunes IDs and load it into an object for use"""
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

def import_books_from_csv():
    """Reads in the CSV and using the Django model objects to populate the DB"""
    
    #Open Book File for Import
    bookCSVFile = open(settings.DATALOAD_DIR + "podiobooks_legacy_book_table.csv")
    
    #Parse the Book File CSV into a dictionary based on the first row values
    bookCSVReader = csv.DictReader(bookCSVFile, dialect='excel')
    
    #PRE CLEANOUT
    Title.objects.all().delete()
    TitleContributor.objects.all().delete()
    Contributor.objects.all().delete()
    
    create_titles_from_book_rows(bookCSVReader)
 
def create_titles_from_book_rows(title_list):
    """Takes a list of title rows from a database query or a CSV file read and creates Title objects"""
    
    libsyn_id_cache = get_libsyn_id_cache()  #Load the Libsyn ID Cache from its CSV
    itunes_id_cache = get_itunes_id_cache()  #Load the iTunes ID Cache from its CSV
    
    # Loop through the rest of the rows in the CSV
    for row in title_list:
        
        # Look up itunes_id in Cache
        itunes_id = None
        try:
            itunes_id = itunes_id_cache[row['ID']]
        except KeyError:
            try:
                itunes_id = itunes_id_cache[row['Subtitle']]
            except KeyError:
                pass
        
        if (int(row['Enabled']) == 1 and int(row['Standby']) == 0):
            # Create a title object in the database based on the current book row
            title = Title.objects.create (
                id=row['ID'],
                name=row['Title'].replace('\\', ''),
                slug=slugify(row['Title']),
                license=determine_license(row['license']),
                description=row['Description'].replace('\\', ''),
                cover=row['Coverimage'],
                status=1,
                display_on_homepage=boolean_clean(row['DisplayOnHomepage']),
                is_hosted_at_pb=True,
                is_explicit=boolean_clean(row['Explicit']),
                is_complete=boolean_clean(row['Complete']),
                avg_audio_quality=row['AvgAudioQuality'],
                avg_narration=row['AvgNarration'],
                avg_writing=row['AvgWriting'],
                avg_overall=row['AvgOverall'],
                deleted=False,
                podiobooker_blog_url=row['DiscussURL'],
                libsyn_show_id=libsyn_id_cache.get(row['ID'],""),
                itunes_adam_id=itunes_id,
                date_created=row['DateCreated']
            )
            
            """ Contributors """
            contributor_list = contributor_translation.translate_contributor(row['Authors']) #Manual Contributor Lookup Translation
            for contributor in contributor_list:
                contributorObject = get_or_create_contributor(contributor['name'])
                contributorType = get_or_create_contributor_type(contributor['type'])
                TitleContributor.objects.create(title=title, contributor=contributorObject, contributor_type=contributorType)
            print "Title: %s\n\t\tContributors: %s" % (title.name, title.contributors.values('display_name'))
            
            """ Awards """
            award_list = award_translation.translate_award(row['ID']) #Manual Award Lookup Translation
            if award_list:
                for awardSlug in award_list:
                    awardObject = get_or_create_award(awardSlug)
                    title.awards.add(awardObject)
                print "\t\tAwards: %s" % (title.awards.values('name'))
            
            """ Series """
            series_slug = series_translation.translate_series(row['ID']) #Manual Series Lookup Translation
            if series_slug:
                seriesObject = get_or_create_series(series_slug)
                title.series = seriesObject
                print "\t\tSeries: %s" % (title.series.name)
            
            """ Category """
            category = get_category(row['CategoryID'])
            if category:
                TitleCategory.objects.create(title=title,category=category)
                print "\t\tCategories: %s" % (title.categories.values('name'))
                if category.slug == 'erotica':
                    title.is_adult = True
            
            """ Partner """
            partner = get_partner(row['PartnerID'])
            if partner:
                title.partner = partner
                print "\t\tPartner: %s" % (title.partner.name)
                
            title.save()
            
        # @TODO Need to double check what we want to do with URLs to iTunes, etc.
        
        # @TODO Create Media Objects for the URL Fields from the Book Row

##### MAIN FUNCTION TO RUN IF THIS SCRIPT IS CALLED ALONE ###
if __name__ == "__main__":
    import_books_from_csv()
    
    
# HANDY MAPPING REFERENCE
# TITLE MODEL FIELDS
#name = models.CharField(max_length=255)
#series = models.ForeignKey('Series', null=True, blank=True)
#description = models.TextField()
#slug = models.SlugField(max_length=255)
#cover = models.ImageField(upload_to=settings.MEDIA_ROOT)
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
