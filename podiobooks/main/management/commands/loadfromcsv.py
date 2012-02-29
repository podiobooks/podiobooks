from django.core.management.base import BaseCommand, CommandError
from podiobooks.main.dataload import data_cleanup
from podiobooks.main.dataload.pb1_csv_migration.migrate_bookcategorycsv_to_category import *
from podiobooks.main.dataload.pb1_csv_migration.migrate_partnercsv_to_partner import *
from podiobooks.main.dataload.pb1_csv_migration.migrate_bookcsv_to_title import *
from podiobooks.main.dataload.pb1_csv_migration.migrate_chaptercsv_to_episode import *
from podiobooks.main.dataload.pb1_csv_migration.migrate_bookratingcsv_to_title import *
from podiobooks.main.dataload.pb1_csv_migration.extract_libsyn_show_id_cache import *

class Command(BaseCommand):
    args = ''
    help = 'Imports CSV Data Through Models Into DB'

    def handle(self, *args, **options):
        """Reads in an "CSV for Excel" export from phpMyAdmin into a the new Podiobooks Schema"""

        # IMPORT CATEGORIES
        importBookCategoriesFromCSV()

        # IMPORT PARTNERS
        importPartnersFromCSV()

        # IMPORT BOOKS
        importBooksFromCSV()

        # IMPORT CHAPTERS
        importChaptersFromCSV()

        # IMPORT RATINGS
        importRatingsFromCSV()

        # UPDATE LIBSYN SHOW ID CACHE
        extractLibsynShowIdCache()

        self.stdout.write('Imported all Data\n')