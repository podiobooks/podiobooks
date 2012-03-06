"""Make calls to live PB1 database to download a CSV extract for use in loading PB2 structures"""

from django.db import connections
from unicode_writer import UnicodeWriter
from django.conf import settings

DATALOAD_DIR = settings.DATALOAD_DIR

def get_book_data(cursor):
    """Make call to PB1 Database and pull SQL data, then write out to CSV"""

    cursor.execute("SELECT * FROM book WHERE enabled = 1 AND standby = 0")

    books = cursor.fetchall()

    if len(books) > 0:
        book_output_file = open(DATALOAD_DIR + 'podiobooks_legacy_book_table.csv', 'w')

        csv_writer = UnicodeWriter(book_output_file)

        # Print out the Title Row
        csv_writer.writerow(
            ["ID", "Title", "DateCreated", "Enabled", "AvgRating", "Description", "Authors", "Webpage", "FeedURL",
             "UserID", "Coverimage", "DisplayOnHomepage", "CategoryID", "Explicit", "Subtitle", "Standby", "Complete",
             "DiscussURL", "Notes", "BookISBN", "AudioISBN", "ITunesLink", "EBookLink", "LuluLink", "PartnerID",
             "DynamicAds", "AvgAudioQuality", "AvgNarration", "AvgWriting", "AvgOverall", "license", "itunescategory",
             "FullLocation", "FullLength", "FullPrice"])

        for book in books:
            csv_writer.writerow(book)

        print ('%d books output into the csv file.' % len(books))
    else:
        print ('No new books to load.')


def get_bookcategory_data(cursor):
    """Get the PB1 Book to Category Data"""

    cursor.execute("SELECT * FROM bookcategory")

    bookcategory_output_file = open(DATALOAD_DIR + 'podiobooks_legacy_bookcategory_table.csv', 'w')

    csv_writer = UnicodeWriter(bookcategory_output_file)

    # Print out the Title Row
    csv_writer.writerow(["ID", "Name", "ParentCatID", "Display", "ITunesXML"])

    bookcategories = cursor.fetchall()

    for bookcategory in bookcategories:
        csv_writer.writerow(bookcategory)

    print ('%d bookcategories output into the csv file' % len(bookcategories))


def get_bookrating_data(cursor):
    """Get the PB1 Book Rating Data"""

    cursor.execute(
        "SELECT bookrating.* FROM bookrating, book WHERE bookrating.bookid = book.id AND book.enabled = 1 AND book.standby = 0")

    bookrating_output_file = open(DATALOAD_DIR + 'podiobooks_legacy_bookrating_table.csv', 'w')

    csv_writer = UnicodeWriter(bookrating_output_file)

    # Print out the Title Row
    csv_writer.writerow(
        ["RatingID", "BookID", "AudioQuality", "Narration", "Writing", "Overall", "UserID", "DateCreated",
         "DateModified"])

    bookratings = cursor.fetchall()

    for bookrating in bookratings:
        csv_writer.writerow(bookrating)

    print ('%d bookratings output into the csv file' % len(bookratings))


def get_chapter_data(cursor):
    """Get the PB1 Chapter Data"""

    cursor.execute(
        "SELECT chapter.* FROM chapter, book WHERE chapter.bookid = book.id AND book.enabled = 1 AND book.standby = 0 AND chapter.enabled = 1")

    chapter_output_file = open(DATALOAD_DIR + 'podiobooks_legacy_chapter_table.csv', 'w')

    csv_writer = UnicodeWriter(chapter_output_file)

    # Print out the Title Row
    csv_writer.writerow(
        ["ID", "BookID", "Sequence", "ShowNotes", "Filename", "DateCreated", "DateUpdated", "Enabled", "StatusID",
         "Bitrate", "Title", "Length", "Format", "NumDownloads"])

    chapters = cursor.fetchall()

    for chapter in chapters:
        csv_writer.writerow(chapter)

    print ('%d chapters output into the csv file' % len(chapters))


def get_partner_data(cursor):
    """Get the PB1 Partner Data"""

    cursor.execute("SELECT * FROM partner")

    partner_output_file = open(DATALOAD_DIR + 'podiobooks_legacy_partner_table.csv', 'w')

    csv_writer = UnicodeWriter(partner_output_file)

    # Print out the Title Row
    csv_writer.writerow(
        ["ID", "Name", "URL", "Logo", "CSS", "HasLibrary", "enabled", "datecreated", "HeaderHTML", "FooterHTML"])

    partners = cursor.fetchall()

    for partner in partners:
        csv_writer.writerow(partner)

    print ('%d partners output into the csv file' % len(partners))


##### MAIN FUNCTION TO RUN IF THIS SCRIPT IS CALLED ALONE ###
if __name__ == "__main__":
    DB_CURSOR = connections['pb1prod'].cursor()
    get_partner_data(DB_CURSOR)
    get_bookcategory_data(DB_CURSOR)
    get_book_data(DB_CURSOR)
    get_chapter_data(DB_CURSOR)
    get_bookrating_data(DB_CURSOR)
    