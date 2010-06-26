"""
This script runs the update_byline function on all the titles

##############################################
#######-----Title Byline Updater-------#######
##############################################
"""

from podiobooks.main.models import Title, TitleContributor, update_byline

def updateBylines():
    titles = Title.objects.all()
    for title in titles:
        print title.name
        titlecontributor = title.titlecontributors.all()[0]
        update_byline(TitleContributor, instance=titlecontributor)

##### MAIN FUNCTION TO RUN IF THIS SCRIPT IS CALLED ALONE ###
if __name__ == "__main__":
    updateBylines()