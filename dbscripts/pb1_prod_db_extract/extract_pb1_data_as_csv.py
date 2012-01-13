from django.db import connections, transaction
import csv
from unicode_writer import UnicodeWriter
from django.conf import settings

DATALOAD_DIR = settings.DATALOAD_DIR

def get_book_data(cursor):
    
    cursor.execute("SELECT * FROM book WHERE enabled = 1 AND standby = 0")
    
    books = cursor.fetchall()
    
    if len(books) > 0:
        book_output_file = open (DATALOAD_DIR + 'podiobooks_legacy_book_table.csv', 'w')
        
        csvWriter = UnicodeWriter(book_output_file)
        
        # Print out the Title Row
        csvWriter.writerow( ["ID","Title","DateCreated","Enabled","AvgRating","Description","Authors","Webpage","FeedURL","UserID","Coverimage","DisplayOnHomepage","CategoryID","Explicit","Subtitle","Standby","Complete","DiscussURL","Notes","BookISBN","AudioISBN","ITunesLink","EBookLink","LuluLink","PartnerID","DynamicAds","AvgAudioQuality","AvgNarration","AvgWriting","AvgOverall","license","itunescategory","FullLocation","FullLength","FullPrice"])
        
        for book in books:
            csvWriter.writerow(book)
        
        print ('%d books output into the csv file.' % len(books))
    else:
        print ('No new books to load.')
    
def get_bookcategory_data(cursor):
    
    cursor.execute("SELECT * FROM bookcategory")
    
    bookcategory_output_file = open (DATALOAD_DIR + 'podiobooks_legacy_bookcategory_table.csv', 'w')
    
    csvWriter = UnicodeWriter(bookcategory_output_file)
    
    # Print out the Title Row
    csvWriter.writerow( ["ID","Name","ParentCatID","Display","ITunesXML"] )
    
    bookcategories = cursor.fetchall()
    
    for bookcategory in bookcategories:
        csvWriter.writerow(bookcategory)
    
    print ('%d bookcategories output into the csv file' % len(bookcategories))
    
def get_bookrating_data(cursor):
    
    cursor.execute("SELECT bookrating.* FROM bookrating, book WHERE bookrating.bookid = book.id AND book.enabled = 1 AND book.standby = 0")
    
    bookrating_output_file = open (DATALOAD_DIR + 'podiobooks_legacy_bookrating_table.csv', 'w')
    
    csvWriter = UnicodeWriter(bookrating_output_file)
    
    # Print out the Title Row
    csvWriter.writerow( ["RatingID","BookID","AudioQuality","Narration","Writing","Overall","UserID","DateCreated","DateModified"] )
    
    bookratings = cursor.fetchall()
    
    for bookrating in bookratings:
        csvWriter.writerow(bookrating)
    
    print ('%d bookratings output into the csv file' % len(bookratings))
    
def get_chapter_data(cursor):
    
    cursor.execute("SELECT chapter.* FROM chapter, book WHERE chapter.bookid = book.id AND book.enabled = 1 AND book.standby = 0 AND chapter.enabled = 1")
    
    chapter_output_file = open (DATALOAD_DIR + 'podiobooks_legacy_chapter_table.csv', 'w')
    
    csvWriter = UnicodeWriter(chapter_output_file)
    
    # Print out the Title Row
    csvWriter.writerow( ["ID","BookID","Sequence","ShowNotes","Filename","DateCreated","DateUpdated","Enabled","StatusID","Bitrate","Title","Length","Format","NumDownloads"] )
    
    chapters = cursor.fetchall()
    
    for chapter in chapters:
        csvWriter.writerow(chapter)
    
    print ('%d chapters output into the csv file' % len(chapters))
    
def get_partner_data(cursor):
    
    cursor.execute("SELECT * FROM partner")
    
    partner_output_file = open (DATALOAD_DIR + 'podiobooks_legacy_partner_table.csv', 'w')
    
    csvWriter = UnicodeWriter(partner_output_file)
    
    # Print out the Title Row
    csvWriter.writerow( ["ID","Name","URL","Logo","CSS","HasLibrary","enabled","datecreated","HeaderHTML","FooterHTML"] )
    
    partners = cursor.fetchall()
    
    for partner in partners:
        csvWriter.writerow(partner)
    
    print ('%d partners output into the csv file' % len(partners))


##### MAIN FUNCTION TO RUN IF THIS SCRIPT IS CALLED ALONE ###
if __name__ == "__main__":
    cursor = connections['pb1prod'].cursor()
    get_partner_data(cursor)
    get_bookcategory_data(cursor)
    get_book_data(cursor)
    get_chapter_data(cursor)
    get_bookrating_data(cursor)
    