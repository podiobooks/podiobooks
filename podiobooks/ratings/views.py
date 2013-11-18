""" Django Views for Ratings"""
import pickle
import json

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.cache import cache
from django.http import HttpResponse
from django.template import RequestContext, Template
from django.views.generic import View
from django.db.models import F
from django.conf import settings
from django.views.decorators.cache import never_cache
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_protect

from podiobooks.ratings.util import get_ratings_widget_dict
from podiobooks.core.views import Title

from django.middleware.csrf import get_token


@never_cache
@csrf_protect
def get_ratings(request, slug):
    """Returns rating for a title as a json response"""

    # since there is no actual form associated with the ratings stuff
    # this will manually fire up a csrftoken cookie
    get_token(request)

    if not request.is_ajax():
        return HttpResponse(json.dumps({"status": "ok"}), mimetype='application/json')

    try:
        in_storage = int(request.GET.get("in_storage", False))
    except ValueError:
        in_storage = False

    try:
        title = Title.objects.get(slug=slug, deleted=False)
    except ObjectDoesNotExist:
        return HttpResponse(json.dumps({"status": "error", "message": "Title not found"}), mimetype='application/json')

    resp = get_ratings_widget_dict(request, title, in_storage)
    return HttpResponse(json.dumps(resp), mimetype='application/json')


class RateTitleView(View):
    """Rate Title"""

    up = True

    def post(self, request, slug, up=True):
        """Add an upvote/downvote for a specific title"""

        if not request.is_ajax():
            return HttpResponse(json.dumps({"status": "ok"}), mimetype='application/json')

        try:
            title = Title.objects.get(slug=slug, deleted=False)
        except ObjectDoesNotExist:
            return HttpResponse(json.dumps({"status": "error", "message": "Title not found"}), mimetype='application/json')

        try:
            in_storage = int(request.POST.get("in_storage", False))
        except ValueError:
            in_storage = False

        ip = str(request.META['REMOTE_ADDR'])
        ip_title_list = cache.get(ip, default={})

        rating = 0
        if ip_title_list and ip_title_list.has_key(title.pk):
            rating = ip_title_list[title.pk]

        # Fresh Vote
        if rating == 0:
            if up:
                ip_title_list[title.pk] = 1
                title.promoter_count += 1
            else:
                ip_title_list[title.pk] = -1
                title.detractor_count += 1

            cache.set(ip, ip_title_list, 100000000)

            if not in_storage:
                title.save()

        # Changing vote from detract to promote
        if up and rating == -1:
            ip_title_list[title.pk] = 1
            title.promoter_count += 1
            title.detractor_count -= 1

            cache.set(ip, ip_title_list, 100000000)

            if not in_storage:
                title.save()

        # Changing vote from promote to detract
        if not up and rating == 1:
            ip_title_list[title.pk] = -1
            title.promoter_count -= 1
            title.detractor_count += 1

            cache.set(ip, ip_title_list, 100000000)

            if not in_storage:
                title.save()

        resp = get_ratings_widget_dict(request, title, in_storage=1 if up else -1)
        return HttpResponse(json.dumps(resp), mimetype='application/json')
