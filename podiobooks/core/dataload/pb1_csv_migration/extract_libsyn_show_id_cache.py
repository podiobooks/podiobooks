"""
This script exports a CSV mapping file of the title_id to libsyn_id mapping so we don't have to go to libsyn every time we load data

##############################################
####----Libsyn ID Cache Extractor-------######
##############################################
"""

# pylint: disable=E0611,F0401,W0401,W0614

import csv
from podiobooks.core.models import *
from podiobooks.core.dataload.pb1_prod_db_extract.unicode_writer import UnicodeWriter
from django.conf import settings

DATALOAD_DIR = settings.DATALOAD_DIR

## Main Function ##
def extract_libsyn_showid_cache():
    titles = Title.objects.exclude(libsyn_show_id="").values_list('id', 'libsyn_show_id')
    print titles
    
    if len(titles) > 0:
        cache_output_file = open (DATALOAD_DIR + 'podiobooks_libsyn_id_cache.csv', 'w')
        
        csv_writer = UnicodeWriter(cache_output_file)
        
        # Print out the Title Row
        csv_writer.writerow( ["ID","LibsynShowId"])
        
        for title in titles:
            csv_writer.writerow(title)
        
        print ('%d libsyn ids output into the csv file.' % len(titles))
    else:
        print ('No new ids to cache.')


##### MAIN FUNCTION TO RUN IF THIS SCRIPT IS CALLED ALONE ###
if __name__ == "__main__":
    """extract libsyn ids from libsyn for podiobooks titles"""
    extract_libsyn_showid_cache()
