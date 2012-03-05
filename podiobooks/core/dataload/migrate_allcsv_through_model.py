"""This script reads in an "CSV for Excel" export from phpMyAdmin into a the new Podiobooks Schema"""

# pylint: disable=E0611,F0401,W0401,W0614

from podiobooks.core.dataload.data_cleanup import *
from pb1_csv_migration.migrate_bookcategorycsv_to_category import *
from pb1_csv_migration.migrate_partnercsv_to_partner import *
from pb1_csv_migration.migrate_bookcsv_to_title import *
from pb1_csv_migration.migrate_chaptercsv_to_episode import *
from pb1_csv_migration.migrate_bookratingcsv_to_title import *
from pb1_csv_migration.extract_libsyn_show_id_cache import *

# IMPORT CATEGORIES
import_book_categories_from_csv()

# IMPORT PARTNERS
import_partners_from_csv()

# IMPORT BOOKS
import_books_from_csv()

# IMPORT CHAPTERS
import_chapters_from_csv()

# IMPORT RATINGS
import_ratings_from_csv()

# UPDATE LIBSYN SHOW ID CACHE
extract_libsyn_showid_cache()