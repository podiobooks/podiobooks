""" Django Views for Ratings"""

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.http import HttpResponse
from django.views.generic import View
from podiobooks.core.views import Title
from django.db.models import F

class RateTitleView(View):
    """Rate Title"""

    up = True

    def get(self, request, pk=None, up=True):
        """Add an upvote/downvote for a specific title"""

        # Add IP check based on Request, Cookie Check

        try:
            title = Title.objects.get(pk=pk)

            if up:
                title.promoter_count = F('promoter_count') + 1
            else:
                title.detractor_count = F('detractor_count') + 1

            #title.save() # Commented out until security can be put in place.

            title = Title.objects.get(pk=pk)

            return HttpResponse("[{0}, {1}]".format(title.promoter_count, title.detractor_count), mimetype='text/plain')

        except ObjectDoesNotExist or MultipleObjectsReturned:
            return HttpResponse("[]", mimetype='text/plain')

