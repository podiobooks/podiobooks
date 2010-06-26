"""
This script runs the update_category_list function on all the titles

##############################################
#######-----Title Caetgory List Updater-------#######
##############################################
"""

from podiobooks.main.models import Title, TitleCategory, update_category_list

def updateCategoryLists():
    titles = Title.objects.all()
    for title in titles:
        print title.name
        titlecategory = title.titlecategories.all()[0]
        update_category_list(TitleCategory, instance=titlecategory)

##### MAIN FUNCTION TO RUN IF THIS SCRIPT IS CALLED ALONE ###
if __name__ == "__main__":
    updateCategoryLists()