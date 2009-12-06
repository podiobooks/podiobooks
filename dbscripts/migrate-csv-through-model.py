"""This script reads in an "CSV for Excel" export from phpMyAdmin into a the new Podiobooks Schema"""

import csv # first we need import necessary lib:csv
from podiobooks.main.models import *
from django.template.defaultfilters import slugify

#First, define several helper functions

def booleanClean(data):
    """Function to check fields that we need to convert to boolean"""
    if (data == None) or (data == ''):
        return 0
    else:
        return int(data)

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

def getOrCreateContributor(contributorName):
    try:
        firstNameGuess, lastNameGuess = contributorName.replace('\\','').split(" ")[:2]
    except:
        firstNameGuess = ""
        lastNameGuess = contributorName
        
    contributor, created = Contributor.objects.get_or_create(display_name=contributorName,
                  defaults={'slug': slugify(contributorName), 'first_name': firstNameGuess, 'last_name': lastNameGuess})
    return contributor

def getOrCreateContributorType(contributorType):
    contributorType, created = ContributorType.objects.get_or_create(slug='author',
                  defaults={'name': 'Author',})
    return contributorType

# Now, begin reading in the CSV and using the Django model objects to populate the DB

#Open Book File for Import
booksCSVFile=open("podiobooks_legacy_book_table.csv") #prepare a csv file for our example

#Parse the Book File CSV into a dictionary based on the first row values
bookCSVReader=csv.DictReader(booksCSVFile,dialect='excel')

#Pull off the first row of the book file as the labels
labelRow = bookCSVReader.next()
print labelRow

#PRE CLEANOUT
Title.objects.all().delete()
TitleContributors.objects.all().delete()
Contributor.objects.all().delete()

# Loop through the rest of the rows in the CSV
for row in bookCSVReader:
    row = row
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
    print "title:",
    print title.name,
    print ": ",
    print title.slug
    mainContributor = getOrCreateContributor(row['Authors'][:48])
    contributorType = getOrCreateContributorType('Author')
    TitleContributors.objects.create(title=title,contributor=mainContributor,contributor_type=contributorType)
    title.save()
    
    # Create URL Objects for the URL Fields from the Book Row


    