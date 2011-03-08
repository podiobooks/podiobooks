"""Django Views for the Social (Twitter, etc.) Module"""

# pylint: disable=R0801

from django.shortcuts import render_to_response
from django.template import RequestContext
from podiobooks.social.twitter_utils import search

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
