

from django.template.loader import render_to_string
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist

from podiobooks.core.views import Title


def get_ratings_widget_dict(request, title, in_storage=False):

    resp = {"status": "ok"}

    ip = str(request.META['REMOTE_ADDR'])
    ip_title_list = cache.get(ip)

    rating = 0
    if ip_title_list and ip_title_list.has_key(title.pk):
        rating = ip_title_list[title.pk]


    # The following setups become honeypots for voting:
    #   to prevent abuse
    #   while letting the user perceive their actions as votes

    # if there is no rating based on IP
    #   But we received one from storage
    #   spit back a widget based on the rating from storage
    if rating == 0:
        if in_storage:
            rating = in_storage

    # if there is an IP-based rating
    #   but there was nothing in storage
    #   spit back a fresh widget
    # if there is a mismatch between storage and IP
    #   spit back a widget showing vote from storage
    else:
        if not in_storage:
            rating = 0
        else:
            rating = in_storage

    # End honeypots

    resp = {
        "promotors": title.promoter_count,
        "detrators": title.detractor_count,
        "widget": render_to_string(
            "ratings/widget.html",
            {"rating": rating, "title": title, "total_ratings": title.promoter_count + title.detractor_count}
        ),
        "userRating": rating,
        "titleSlug": title.slug
    }

    return resp


def get_rating_from_storage(request):
    """
    return the current rating
    from local storage in user's browser

    returns False if unavailable or invalid
    """

    # in_storage is the old vote (if there was one)
    try:
        in_storage = int(request.REQUEST.get("in_storage", False))
        if in_storage != -1 and in_storage != 1:
            in_storage = False
    except ValueError:
        in_storage = False

    return in_storage
