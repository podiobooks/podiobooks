from django.shortcuts import render_to_response
from django.template import RequestContext
from twitter_utils import search

""" Views """

def twitter_search(request, keywords=None):
    """
    Twitter Search Results

    url: /
    
    template : templates/social/twitter_search.html
    """
    
    tweets = search(keywords)
    
    response_data = {'tweets': tweets,
                     }
    
    return render_to_response('social/twitter_search.html', response_data, context_instance=RequestContext(request))