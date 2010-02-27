"""This script reads in an "CSV for Excel" export from phpMyAdmin into a the new Podiobooks Schema"""

# IMPORT CATEGORIES
from migrate_bookcategorycsv_to_category import *
importBookCategories()

# IMPORT PARTNERS
from migrate_partnercsv_to_partner import *
importPartners()

# IMPORT BOOKS
from migrate_bookcsv_to_title import *
importBooks()

# IMPORT CHAPTERS
from migrate_chaptercsv_to_episode import *
importChapters()

# IMPORT RATINGS
from migrate_bookratingcsv_to_title import *
importRatings()
 
