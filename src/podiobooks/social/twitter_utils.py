from twitter import Twitter
import pprint

def search(keywords):
    twitter_search = Twitter(domain="search.twitter.com")
    
    response = twitter_search.search(q=keywords)
    
    if response:
        return response['results']
    else:
        return None

##### MAIN FUNCTION TO RUN IF THIS SCRIPT IS CALLED ALONE ###
if __name__ == "__main__":
    result = search("Shadowmagic")
    
    # pretty print the result
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(result)