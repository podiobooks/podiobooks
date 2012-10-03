#1048167

#http://www.goodreads.com/author/show/18541.xml?key=AMbKgFwD8eW38AknGAXLVw

"""General Utilities for working with the Goodreads API"""

import urllib
from xml.etree import ElementTree

GOODREADS_API_URL = 'http://www.goodreads.com/author/show/'
GOODREADS_API_KEY = 'AMbKgFwD8eW38AknGAXLVw'

def get_author_info(author_id):
    """ Returns info from Goodreads about a certain author """

    author_xml = urllib.urlopen("{0}{1}.xml?key={2}".format(GOODREADS_API_URL, author_id, GOODREADS_API_KEY))

    result = ElementTree.parse(author_xml).getroot().find('author')

    print result.find('image_url').text
    print result.find('about').text
    print result.find('link').text

if __name__ == "__main__":
    get_author_info('1048167')