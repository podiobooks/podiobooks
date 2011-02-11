"""Utility Functions For Calling the Twitter API"""

import twitter

def search(keywords):
    """Search the twitter timeline for keywords"""
    twitter_api = twitter.Api()
    response = twitter_api.GetSearch(term=keywords)
    
    if response:
        return response
    else:
        return None  # pragma: no cover

def main(): # pragma: no cover
    """MAIN FUNCTION TO RUN IF THIS SCRIPT IS CALLED ALONE"""
    
    statuses = search("Shadowmagic")
    
    if statuses:
        for status in statuses:
            print status.user.screen_name + ':',
            print status.text
            print '---------'
    
    return statuses
    
if __name__ == "__main__":
    main()  # pragma: no cover