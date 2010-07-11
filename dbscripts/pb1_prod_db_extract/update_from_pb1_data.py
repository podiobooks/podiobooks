from django.db import connections, transaction
import csv, cStringIO, codecs
from podiobooks.main.models import Title, Category, Episode, Partner, Rating
from django.db.models import Max
from pb1_csv_migration.migrate_bookcsv_to_title import createTitlesFromRows
from pb1_csv_migration.migrate_chaptercsv_to_episode import createEpisodesFromRows
from pb1_csv_migration.migrate_bookratingcsv_to_title import createRatingsFromRows
from itertools import izip

def get_book_data(cursor, last_book_id):
    cursor.execute("SELECT * FROM book WHERE enabled = 1 AND standby = 0 AND id > %s", [last_book_id,])

    col_names = [desc[0] for desc in cursor.description]
    
    books = []
    
    """ Merges the col names and data into a dictionary object """
    while True:
        row = cursor.fetchone()
        if row is None:
            break
        row_dict = dict(izip(col_names, row))
        books.append(row_dict)
    
    if len(books) > 0:
        print ('%d books need to be loaded.' % len(books))
        createTitlesFromRows(books)
    else:
        print ('No new books needs to be loaded.')

def get_chapter_data(cursor, last_chapter_id):
    cursor.execute("SELECT chapter.* FROM chapter, book WHERE chapter.bookid = book.id AND book.enabled = 1 AND book.standby = 0 AND chapter.id > %s", [last_chapter_id,])

    col_names = [desc[0] for desc in cursor.description]
    
    chapters = []
    
    """ Merges the col names and data into a dictionary object """
    while True:
        row = cursor.fetchone()
        if row is None:
            break
        row_dict = dict(izip(col_names, row))
        chapters.append(row_dict)
    
    if len(chapters) > 0:
        print ('%d episodes need to be loaded.' % len(chapters))
        createEpisodesFromRows(chapters)
    else:
        print ('No new episodes needs to be loaded.')
        
def get_ratings_data(cursor, last_rating_id):
    cursor.execute("SELECT bookrating.* FROM bookrating, book WHERE bookrating.bookid = book.id AND book.enabled = 1 AND book.standby = 0 AND bookrating.ratingid > %s", [last_rating_id,])

    col_names = [desc[0] for desc in cursor.description]
    
    ratings = []
    
    """ Merges the col names and data into a dictionary object """
    while True:
        row = cursor.fetchone()
        if row is None:
            break
        row_dict = dict(izip(col_names, row))
        ratings.append(row_dict)
    
    if len(ratings) > 0:
        print ('%d ratings need to be loaded.' % len(ratings))
        createRatingsFromRows(ratings)
    else:
        print ('No new ratings need to be loaded.')

def get_max_book_id():
    max_id_results = Title.objects.aggregate(max_id=Max('id'))
    return max_id_results['max_id']

def get_max_episode_id():
    max_id_results = Episode.objects.aggregate(max_id=Max('id'))
    return max_id_results['max_id']

def get_max_rating_id():
    max_id_results = Rating.objects.aggregate(max_id=Max('last_rating_id'))
    return max_id_results['max_id']

def get_max_category_id():
    max_id_results = Category.objects.aggregate(max_id=Max('id'))
    return max_id_results['max_id']

def get_max_partner_id():
    max_id_results = Partner.objects.aggregate(max_id=Max('id'))
    return max_id_results['max_id']

##### MAIN FUNCTION TO RUN IF THIS SCRIPT IS CALLED ALONE ###
if __name__ == "__main__":
    cursor = connections['pb1prod'].cursor()
    get_book_data(cursor, get_max_book_id())
    get_chapter_data(cursor, get_max_episode_id())
    get_ratings_data(cursor, get_max_rating_id())
    