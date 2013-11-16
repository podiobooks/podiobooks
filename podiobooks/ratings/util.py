

from django.template.loader import render_to_string
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist

from podiobooks.core.views import Title


def get_ratings_widget_dict(request, title):

    resp = {"status": "ok"}

    ip = str(request.META['REMOTE_ADDR'])
    ip_title_list = cache.get(ip)

    rating = 0
    if ip_title_list and ip_title_list.has_key(title.pk):
        rating = ip_title_list[title.pk]

    resp = {
        "promotors": title.promoter_count,
        "detrators": title.detractor_count,
        "widget": render_to_string(
            "ratings/widget.html",
            {"rating": rating, "title": title}
        )
    }

    return resp
