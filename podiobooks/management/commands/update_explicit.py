"""Load the Explicit Data Into the DB"""

import os, csv
from django.conf import settings
from django.core.management.base import NoArgsCommand
from podiobooks.core.models import Title

class Command(NoArgsCommand):
    """
        Load the Explicit Data Into the DB
    """
    help = "Load the Explicit Data Into the DB"

    def handle_noargs(self, **options):
        load_file = os.path.join(settings.PROJECT_ROOT, 'core', 'fixtures', 'podiobooks_explicit_data.csv')
        explicit_csv_file = open(load_file)

        #Parse the Explicit File CSV into a dictionary based on the first row values
        title_list = csv.DictReader(explicit_csv_file, dialect='excel')

        for row in title_list:
            try:
                title = Title.objects.get(pk=row.get('ID'))
            except:
                break

            title.is_for_kids = eval(row.get('Is_For_Kids'))
            title.is_family_friendly = eval(row.get('Is_Family_Friendly'))
            title.is_explicit = eval(row.get('Is_Explicit'))

            title.save()

        explicit_csv_file.close()


