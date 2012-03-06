"""Update PB2 database based on latest live PB1 Data"""

from django.db import connections
from podiobooks.core.models import Title, Category, Episode, Partner, Rating
from django.db.models import Max
from podiobooks.core.dataload.pb1_csv_migration.migrate_bookcsv_to_title import create_titles_from_book_rows
from podiobooks.core.dataload.pb1_csv_migration.migrate_chaptercsv_to_episode import create_episodes_from_rows
from podiobooks.core.dataload.pb1_csv_migration.migrate_bookratingcsv_to_title import create_ratings_from_rows
from itertools import izip

def get_book_data(cursor, last_book_id):
    """Get Book Data from Live PB1 Database"""
    cursor.execute("SELECT * FROM book WHERE enabled = 1 AND standby = 0 AND id > %s", [last_book_id,])

    col_names = [desc[0] for desc in cursor.description]
    
    books = []
    
    # Merges the col names and data into a dictionary object
    while True:
        row = cursor.fetchone()
        if row is None:
            break
        row_dict = dict(izip(col_names, row))
        books.append(row_dict)
    
    if len(books) > 0:
        print ('%d books need to be loaded.' % len(books))
        create_titles_from_book_rows(books)
    else:
        print ('No new books needs to be loaded.')

def get_chapter_data(cursor, last_chapter_id):
    """Get Chapter Data from Live PB1 Database"""
    cursor.execute("SELECT chapter.* FROM chapter, book WHERE chapter.bookid = book.id AND book.enabled = 1 AND book.standby = 0 AND chapter.id > %s", [last_chapter_id,])

    col_names = [desc[0] for desc in cursor.description]
    
    chapters = []
    
    # Merges the col names and data into a dictionary object
    while True:
        row = cursor.fetchone()
        if row is None:
            break
        row_dict = dict(izip(col_names, row))
        chapters.append(row_dict)
    
    if len(chapters) > 0:
        print ('%d episodes need to be loaded.' % len(chapters))
        create_episodes_from_rows(chapters)
    else:
        print ('No new episodes needs to be loaded.')
        
def get_ratings_data(cursor, last_rating_id):
    """Get Ratings Data from Live PB1 Database"""
    cursor.execute("SELECT bookrating.* FROM bookrating, book WHERE bookrating.bookid = book.id AND book.enabled = 1 AND book.standby = 0 AND bookrating.ratingid > %s", [last_rating_id,])

    col_names = [desc[0] for desc in cursor.description]
    
    ratings = []
    
    # Merges the col names and data into a dictionary object
    while True:
        row = cursor.fetchone()
        if row is None:
            break
        row_dict = dict(izip(col_names, row))
        ratings.append(row_dict)
    
    if len(ratings) > 0:
        print ('%d ratings need to be loaded.' % len(ratings))
        create_ratings_from_rows(ratings)
    else:
        print ('No new ratings need to be loaded.')

def get_max_book_id():
    """Get Max Book ID Currently Loaded"""
    max_id_results = Title.objects.aggregate(max_id=Max('id'))
    return max_id_results['max_id']

def get_max_episode_id():
    """Get Max Episode ID Currently Loaded"""
    max_id_results = Episode.objects.aggregate(max_id=Max('id'))
    return max_id_results['max_id']

def get_max_rating_id():
    """Get Max Rating ID Currently Loaded"""
    max_id_results = Rating.objects.aggregate(max_id=Max('last_rating_id'))
    return max_id_results['max_id']

def get_max_category_id():
    """Get Max Category ID Currently Loaded"""
    max_id_results = Category.objects.aggregate(max_id=Max('id'))
    return max_id_results['max_id']

def get_max_partner_id():
    """Get Max partner ID Currently Loaded"""
    max_id_results = Partner.objects.aggregate(max_id=Max('id'))
    return max_id_results['max_id']

##### MAIN FUNCTION TO RUN IF THIS SCRIPT IS CALLED ALONE ###
if __name__ == "__main__":
    DB_CURSOR = connections['pb1prod'].cursor()
    get_book_data(DB_CURSOR, get_max_book_id())
    get_chapter_data(DB_CURSOR, get_max_episode_id())
    get_ratings_data(DB_CURSOR, get_max_rating_id())
    