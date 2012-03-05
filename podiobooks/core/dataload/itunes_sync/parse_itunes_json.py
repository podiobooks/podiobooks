"""Import JSON Data Structure from iTunes to grab iTunes IDs for podiobooks titles"""

import json
from django.conf import settings

def parse_itunes_json():
    # Open File for parsing
    itunes_json_file = open(settings.DATALOAD_DIR + "podiobooks_itunes_data.json")
    itunes_json = itunes_json_file.read()

    # Fix invalid JSON
    itunes_json = itunes_json.replace("{originalFeedURL:", "{\"originalFeedURL\":")
    itunes_json = itunes_json.replace(",artistId:", ",\"artistId\":")
    itunes_json = itunes_json.replace(",title:", ",\"title\":")
    itunes_json = itunes_json.replace(",tags:", ",\"tags\":")
    itunes_json = itunes_json.replace(",lastPublishedDate:", ",\"lastPublishedDate\":")
    itunes_json = itunes_json.replace(",adamId:", ",\"adamId\":")
    itunes_json = itunes_json.replace(",lastChecked:", ",\"lastChecked\":")
    itunes_json = itunes_json.replace(",status:", ",\"status\":")
    itunes_json = itunes_json.replace(",themeName:", ",\"themeName\":")
    itunes_json = itunes_json.replace(",isAppleHosted:", ",\"isAppleHosted\":")
    itunes_json = itunes_json.replace(",contributors:", ",\"contributors\":")
    itunes_json = itunes_json.replace(",brandNew:", ",\"brandNew\":")
    itunes_json = itunes_json.replace(",numItems:", ",\"numItems\":")
    itunes_json = itunes_json.replace(",category:", ",\"category\":")
    itunes_json = itunes_json.replace(",shortFeedError:", ",\"shortFeedError\":")

    itunes_data = json.loads(itunes_json)

    cache_output_file = open (settings.DATALOAD_DIR + 'podiobooks_itunes_id_cache.csv', 'w')

    #svWriter = UnicodeWriter(cache_output_file)

    # Print out the Title Row
    cache_output_file.write("\"ID\",\"Slug\",\"iTunesID\"\n")

    for title in itunes_data:
        title_slug = title['originalFeedURL'].replace("http://www.podiobooks.com/title/",",")
        title_slug = title_slug.replace("/feed/", "")
        title_slug = title_slug.replace("/feed", "")
        title_slug = title_slug.replace("http://www.podiobooks.com/bookfeed/sampler/","")
        title_slug = title_slug.replace("/book.xml",",")
        title_slug = title_slug.replace("http://www.podiobooks.com/api/bookrss2.php?user=sampler&book=","")
        title_slug = title_slug.replace("http://www.podiobooks.com/maint.htmltitle/origin-scroll?user=sampler&book=","")
        cache_output_file.write( "%s,%s\n" % ( title_slug, title['adamId'] ))

##### MAIN FUNCTION TO RUN IF THIS SCRIPT IS CALLED ALONE ###
if __name__ == "__main__":
    """extract itunes ids for podiobooks titles"""
    parse_itunes_json()