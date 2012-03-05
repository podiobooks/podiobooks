""" Django management command to load all data into database from external CSV Files.
In general, you shouldn't need this unless you are working on a new set of dataload scripts, or are tuning them.
You can just use the fixture 'alldata.json.zip' to load up a full set of data into your env.
You can use this script to load fresh from the CSV files, and then do manage.py dumpdata to refresh alldata.json.
"""

# pylint: disable=E0611,F0401,W0401,W0614


from django.core.management.base import BaseCommand, CommandError
from podiobooks.core.dataload import data_cleanup
from podiobooks.core.dataload.pb1_csv_migration.migrate_bookcategorycsv_to_category import *
from podiobooks.core.dataload.pb1_csv_migration.migrate_partnercsv_to_partner import *
from podiobooks.core.dataload.pb1_csv_migration.migrate_bookcsv_to_title import *
from podiobooks.core.dataload.pb1_csv_migration.migrate_chaptercsv_to_episode import *
from podiobooks.core.dataload.pb1_csv_migration.migrate_bookratingcsv_to_title import *
from podiobooks.core.dataload.pb1_csv_migration.extract_libsyn_show_id_cache import *

class Command(BaseCommand):
    args = ''
    help = 'Imports CSV Data Through Models Into DB'

    def handle(self, *args, **options):
        """Reads in an "CSV for Excel" export from phpMyAdmin into a the new Podiobooks Schema"""

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

        self.stdout.write('Imported all Data\n')