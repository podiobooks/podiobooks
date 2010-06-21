"""This script reads in an "CSV for Excel" export from phpMyAdmin into a the new Podiobooks Schema"""

# IMPORT CATEGORIES
from migrate_bookcategorycsv_to_category import *
importBookCategoriesFromCSV()

# IMPORT PARTNERS
from migrate_partnercsv_to_partner import *
importPartnersFromCSV()

# IMPORT BOOKS
from migrate_bookcsv_to_title import *
importBooksFromCSV()

# IMPORT CHAPTERS
from migrate_chaptercsv_to_episode import *
importChaptersFromCSV()

# IMPORT RATINGS
from migrate_bookratingcsv_to_title import *
importRatingsFromCSV()
 
