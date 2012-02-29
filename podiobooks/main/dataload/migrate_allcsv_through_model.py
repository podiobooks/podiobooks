"""This script reads in an "CSV for Excel" export from phpMyAdmin into a the new Podiobooks Schema"""

from data_cleanup import *

# IMPORT CATEGORIES
from pb1_csv_migration.migrate_bookcategorycsv_to_category import *
importBookCategoriesFromCSV()

# IMPORT PARTNERS
from pb1_csv_migration.migrate_partnercsv_to_partner import *
importPartnersFromCSV()

# IMPORT BOOKS
from pb1_csv_migration.migrate_bookcsv_to_title import *
importBooksFromCSV()

# IMPORT CHAPTERS
from pb1_csv_migration.migrate_chaptercsv_to_episode import *
importChaptersFromCSV()

# IMPORT RATINGS
from pb1_csv_migration.migrate_bookratingcsv_to_title import *
importRatingsFromCSV()

# UPDATE LIBSYN SHOW ID CACHE
from pb1_csv_migration.extract_libsyn_show_id_cache import *
extractLibsynShowIdCache()