""" Django Views for Ratings"""
import json

from django.core.exceptions import ObjectDoesNotExist
from django.core.cache import cache
from django.http import HttpResponse

from django.views.generic import View
from django.views.decorators.cache import never_cache

from podiobooks.ratings.util import get_ratings_widget_dict, get_rating_from_storage
from podiobooks.core.views import Title

from django.middleware.csrf import get_token


@never_cache
def get_ratings(request, slug):
    """Returns rating for a title as a json response"""

    # since there is no actual form associated with the ratings stuff
    # this will manually fire up a csrftoken cookie
    get_token(request)

    if not request.is_ajax():
        return HttpResponse(json.dumps({"status": "ok"}), mimetype='application/json')

    in_storage = get_rating_from_storage(request)

    try:
        title = Title.objects.get(slug=slug, deleted=False)
    except ObjectDoesNotExist:
        return HttpResponse(json.dumps({"status": "error", "message": "Title not found"}), mimetype='application/json')

    resp = get_ratings_widget_dict(request, title, in_storage)
    return HttpResponse(json.dumps(resp), mimetype='application/json')


class RateTitleView(View):
    """Rate Title"""

    up_vote = True

    def post(self, request, slug, up_vote=True):
        """Add an upvote/downvote for a specific title"""

        if not request.is_ajax():
            return HttpResponse(json.dumps({"status": "ok"}), mimetype='application/json')

        try:
            title = Title.objects.get(slug=slug, deleted=False)
        except ObjectDoesNotExist:
            return HttpResponse(json.dumps({"status": "error", "message": "Title not found"}), mimetype='application/json')

        in_storage = get_rating_from_storage(request)

        ip_address = "pb-rating-%s" % str(request.META['REMOTE_ADDR'])
        ip_title_list = cache.get(ip_address, default={})

        # rating will hold value for the rating pulled from cache
        rating = 0
        if ip_title_list and ip_title_list.has_key(title.pk):
            rating = ip_title_list[title.pk]

        # corrects for changing vote after changing IP
        if in_storage and rating != in_storage:
            rating = in_storage

        # Fresh Vote
        if rating == 0:
            ip_title_list[title.pk] = 1 if up_vote else -1
            cache.set(ip_address, ip_title_list, 100000000)

            if not in_storage:
                if up_vote:
                    title.promoter_count += 1
                else:
                    title.detractor_count += 1
                title.save()

        # Changing vote from detract to promote
        if up_vote and rating == -1:
            ip_title_list[title.pk] = 1
            cache.set(ip_address, ip_title_list, 100000000)

            if in_storage == -1:
                title.promoter_count += 1
                title.detractor_count -= 1
                title.save()

        # Changing vote from promote to detract
        if not up_vote and rating == 1:
            ip_title_list[title.pk] = -1
            cache.set(ip_address, ip_title_list, 100000000)

            if in_storage == 1:
                title.promoter_count -= 1
                title.detractor_count += 1
                title.save()

        resp = get_ratings_widget_dict(request, title, in_storage=1 if up_vote else -1)
        return HttpResponse(json.dumps(resp), mimetype='application/json')
