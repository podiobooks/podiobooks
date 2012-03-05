"""
This script deletes things from the database to get down to a reduced dataset for fixture dump purposes.

##############################################
#######---Current Database Minimizer---#######
##############################################
"""

from podiobooks.main.models import *
from django.db.models import Q
from django.contrib.comments.models import Comment

#Book/Title Helper Functions

def reduce_data():
    """Function to delete data from the database to get down to a reduced subset"""
    titles_to_delete = Title.objects.exclude(Q(slug='shadowmagic')|Q(slug='earthcore')|Q(slug='trader-tales-4-double-share')|Q(slug='the-plump-buffet'))
    print titles_to_delete
    titles_to_delete.delete()
    
    id_list = Title.objects.all().values('id')
    id_list_strings = []
    for id in id_list:
        id_list_strings.append(str(id['id']))
    print id_list_strings
    
    comments_to_delete = Comment.objects.exclude(object_pk__in=id_list_strings)
    print comments_to_delete
    comments_to_delete.delete()
    
    contributor_list = Contributor.objects.exclude(title__id__in=Title.objects.all())
    print contributor_list
    contributor_list.delete()
    
##### MAIN FUNCTION TO RUN IF THIS SCRIPT IS CALLED ALONE ###
if __name__ == "__main__":
    reduce_data()

