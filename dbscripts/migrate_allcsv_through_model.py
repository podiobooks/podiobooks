"""This script reads in an "CSV for Excel" export from phpMyAdmin into a the new Podiobooks Schema"""

# IMPORT BOOKS
from migrate_bookcsv_to_title import *
importBooks()

# IMPORT CHAPTERS
from migrate_chaptercsv_to_episode import *
importChapters()
 