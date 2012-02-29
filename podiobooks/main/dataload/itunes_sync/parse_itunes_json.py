import json
from django.conf import settings

# Open File for parsing
itunesJsonFile = open(settings.DATALOAD_DIR + "podiobooks_itunes_data.json")
itunesJson = itunesJsonFile.read()

# Fix invalid JSON
itunesJson = itunesJson.replace("{originalFeedURL:", "{\"originalFeedURL\":")
itunesJson = itunesJson.replace(",artistId:", ",\"artistId\":")
itunesJson = itunesJson.replace(",title:", ",\"title\":")
itunesJson = itunesJson.replace(",tags:", ",\"tags\":")
itunesJson = itunesJson.replace(",lastPublishedDate:", ",\"lastPublishedDate\":")
itunesJson = itunesJson.replace(",adamId:", ",\"adamId\":")
itunesJson = itunesJson.replace(",lastChecked:", ",\"lastChecked\":")
itunesJson = itunesJson.replace(",status:", ",\"status\":")
itunesJson = itunesJson.replace(",themeName:", ",\"themeName\":")
itunesJson = itunesJson.replace(",isAppleHosted:", ",\"isAppleHosted\":")
itunesJson = itunesJson.replace(",contributors:", ",\"contributors\":")
itunesJson = itunesJson.replace(",brandNew:", ",\"brandNew\":")
itunesJson = itunesJson.replace(",numItems:", ",\"numItems\":")
itunesJson = itunesJson.replace(",category:", ",\"category\":")
itunesJson = itunesJson.replace(",shortFeedError:", ",\"shortFeedError\":")

itunesData = json.loads(itunesJson)

cache_output_file = open (settings.DATALOAD_DIR + 'podiobooks_itunes_id_cache.csv', 'w')

#svWriter = UnicodeWriter(cache_output_file)

# Print out the Title Row
cache_output_file.write("\"ID\",\"Slug\",\"iTunesID\"\n")

for title in itunesData:
    titleSlug = title['originalFeedURL'].replace("http://www.podiobooks.com/title/",",")
    titleSlug = titleSlug.replace("/feed/", "")
    titleSlug = titleSlug.replace("/feed", "")
    titleSlug = titleSlug.replace("http://www.podiobooks.com/bookfeed/sampler/","")
    titleSlug = titleSlug.replace("/book.xml",",")
    titleSlug = titleSlug.replace("http://www.podiobooks.com/api/bookrss2.php?user=sampler&book=","")
    titleSlug = titleSlug.replace("http://www.podiobooks.com/maint.htmltitle/origin-scroll?user=sampler&book=","")
    cache_output_file.write( "%s,%s\n" % ( titleSlug, title['adamId'] ))