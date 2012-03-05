"""
This script runs the update_category_list function on all the titles to regenerate the on-model cached string of categories

##############################################
####----Title Category List Updater------#####
##############################################
"""

from podiobooks.core.models import Title, TitleCategory, update_category_list

def update_category_lists():
    titles = Title.objects.all()
    for title in titles:
        print title.name
        titlecategory = title.titlecategories.all()[0]
        update_category_list(TitleCategory, instance=titlecategory)

##### MAIN FUNCTION TO RUN IF THIS SCRIPT IS CALLED ALONE ###
if __name__ == "__main__":
    update_category_lists()