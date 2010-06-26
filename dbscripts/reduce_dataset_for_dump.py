"""
This script deletes things from the database to get down to a reduced dataset for fixture dump purposes.

##############################################
#######---Current Database Minimizer---#######
##############################################
"""

from podiobooks.main.models import *

#Book/Title Helper Functions

def reduceData():
    """Function to delete data from the database to get down to a reduced subset"""
    titles_to_delete = Title.objects.exclude(titlecontributors__contributor__slug='nathan-lowell')
    print titles_to_delete
    titles_to_delete.delete()
    
##### MAIN FUNCTION TO RUN IF THIS SCRIPT IS CALLED ALONE ###
if __name__ == "__main__":
    reduceData()

