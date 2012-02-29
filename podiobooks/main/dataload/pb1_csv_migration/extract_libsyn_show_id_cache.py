"""
This script exports a CSV mapping file of the title_id to libsyn_id mapping so we don't have to go to libsyn every time we load data

##############################################
####----Libsyn ID Cache Extractor-------######
##############################################
"""

import csv
from podiobooks.main.models import *
from podiobooks.main.dataload.pb1_prod_db_extract.unicode_writer import UnicodeWriter
from django.conf import settings

DATALOAD_DIR = settings.DATALOAD_DIR

## Main Function ##
def extractLibsynShowIdCache():
    titles = Title.objects.exclude(libsyn_show_id="").values_list('id', 'libsyn_show_id')
    print titles
    
    if len(titles) > 0:
        cache_output_file = open (DATALOAD_DIR + 'podiobooks_libsyn_id_cache.csv', 'w')
        
        csvWriter = UnicodeWriter(cache_output_file)
        
        # Print out the Title Row
        csvWriter.writerow( ["ID","LibsynShowId"])
        
        for title in titles:
            csvWriter.writerow(title)
        
        print ('%d libsyn ids output into the csv file.' % len(titles))
    else:
        print ('No new ids to cache.')


##### MAIN FUNCTION TO RUN IF THIS SCRIPT IS CALLED ALONE ###
if __name__ == "__main__":
    extractLibsynShowIdCache()
