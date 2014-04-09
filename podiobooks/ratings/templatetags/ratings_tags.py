""" Tags used for working with Titles """

from django import template


register = template.Library()


@register.inclusion_tag('ratings/calculation.html')
def show_overall_rating(title):
    """Calculate the overall rating for a title"""
    total = title.promoter_count + title.detractor_count

    if total < 5:
        return {"rating": None}

    rating = float(title.promoter_count) / total

    rating_range = round(rating, 1)

    rating = int(rating * 100)
    rating_range *= 100

    if rating > 100:
        rating = 100

    return {"rating": rating, "rating_range": int(rating_range)}



