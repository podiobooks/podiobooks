from django import template
from pbsite.main.models import *
register = template.Library()

@register.inclusion_tag('main/title/detail.html')
def title_detail(title):
    return { 'title' : title };

@register.inclusion_tag('main/title/show_categories.html')
def show_categories(title):
    categories = title.categories.all()
    return { 'categories' : categories }

@register.inclusion_tag('main/title/list.html')
def title_list(titles):
    return { 'titles' : titles }

@register.simple_tag
def title_class(title):
    ret = "title title_id_%s title_slug_%s" % ( title.id, title.slug )
    for category in title.categories.all():
        ret = ret + " category_%s" % category.slug

    for contType in ContributorType.objects.all():
        for tc in TitleContributors.objects.filter(
            title = title,
            contributor_type = contType):
            ret = ret + " contributor_%s_%s" % ( contType.slug, tc.contributor.slug)


    if (title.awards.count() > 0):
        ret = ret + " award_winner"

    if (title.license != None):
        ret = ret + " license_" % title.license.slug

    return ret



        
