""" Django Custom Template Tags for Ratings-Related Stuff """

from django import template
from podiobooks.ratings.views import already_voted

register = template.Library()

@register.inclusion_tag('ratings/tags/ratings_box.html')
def show_ratings_box(request, title):
    """Ratings Box"""

    if request.GET.get('vote', False):
        already_rated = already_voted(request, title.pk)
    else:
        already_rated = 'Off'

    return {'already_rated': already_rated, 'title': title}
