"""Utility Functions For Calling the Twitter API"""

from twitter import Twitter  # pylint: disable=E0611,F0401
import pprint

def search(keywords):
    """Search the twitter timeline for keywords"""
    twitter_search = Twitter(domain="search.twitter.com")
    
    response = twitter_search.search(q=keywords)
    
    if response:
        return response['results']
    else:
        return None  # pragma: no cover

def main(): # pragma: no cover
    """MAIN FUNCTION TO RUN IF THIS SCRIPT IS CALLED ALONE"""
    
    result = search("Shadowmagic")
    
    # pretty print the result
    pprinter = pprint.PrettyPrinter(indent=4)
    pprinter.pprint(result)
    
    return result
    
if __name__ == "__main__":
    main()  # pragma: no cover