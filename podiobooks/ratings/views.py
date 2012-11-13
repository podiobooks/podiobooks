""" Django Views for Ratings"""

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.cache import cache
from django.http import HttpResponse
from django.views.generic import View
from podiobooks.core.views import Title
from django.db.models import F
import pickle

class RateTitleView(View):
    """Rate Title"""

    up = True

    def get(self, request, pk=None, up=True):
        """Add an upvote/downvote for a specific title"""

        # Add Request.is_ajax() check

        # Use cache to hold IP
        ip_title_list = cache.get(request.META['REMOTE_ADDR'])
        if not ip_title_list:
            cache.set(request.META['REMOTE_ADDR'], [pk,], 10000000)
        elif pk in ip_title_list:
            return HttpResponse("['error':'You have already voted for this title.']", mimetype="application/json")
        else:
            ip_title_list.add(pk)
            cache.set(request.META['REMOTE_ADDR'], ip_title_list, 10000000)

        # Keep a comma-separated, signed cookie of all the titles ever voted for
        # It's possible that someone could hit max cookie length limit here, what then?
        # Also, since the cookies are sent back and forth on each request, this means the more you vote, the slower the site
        vote_cookie = request.get_signed_cookie('v', False)
        if vote_cookie:
            vote_cookie_list = vote_cookie.split(',')
            if pk in vote_cookie_list:
                return HttpResponse("['error':'You have already voted for this title.']", mimetype="application/json")
            else:
                vote_cookie_list.append(pk)
                vote_cookie = ','.join(vote_cookie_list)
        else:
            vote_cookie = str(pk)

        try:
            title = Title.objects.get(pk=pk)

            if up:
                title.promoter_count = F('promoter_count') + 1
            else:
                title.detractor_count = F('detractor_count') + 1

            title.save() # Commented out until security can be put in place.

            title = Title.objects.get(pk=pk)

            response = HttpResponse("[{0}, {1}]".format(title.promoter_count, title.detractor_count), mimetype='application/json')
            response.set_signed_cookie('v', vote_cookie)

            return response

        except ObjectDoesNotExist or MultipleObjectsReturned:
            return HttpResponse("['error':'Title Not Found.']", mimetype='application/json')

